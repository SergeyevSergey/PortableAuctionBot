from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from telegram import InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from lot.models import Lot, UserBid
from lot.materials.keyboards import *
from lot.materials.functions import *
from lot.materials.messages import *


# Starting function
class Command(BaseCommand):
    help = 'Run bot'

    def handle(self, *args, **kwargs):
        # Logics
        updater = Updater(settings.TELEGRAM_BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher

    # Commands

        # /start
        def start(update, context):
            place_restrictions(context)
            user_name = update.effective_user.first_name
            reply_markup = InlineKeyboardMarkup(menu_keyboard)
            send_welcome(update, user_name, reply_markup)

        # /help
        def bot_help(update, context):
            print('asked for help')
            send_help(update)

        # /menu
        def context_menu(update, context):
            place_restrictions(context)
            reply_markup = InlineKeyboardMarkup(menu_keyboard)
            send_menu(update, reply_markup)

        # /cancel
        def cancel_operation(update, context):
            send_cancel(update)
            return context_menu(update, context)

    # Buttons

        # view_last_auctions
        def view_last_auctions_button(update, context):
            # place restrictions
            place_restrictions(context)

            query = update.callback_query
            if query.data == 'view_last':

                # logics
                query.answer()
                query.edit_message_text(text='Searching for lots...')
                recent_lots = Lot.objects.all()
                if 0 < len(recent_lots) <= 5:
                    for lot in recent_lots:

                        # keyboard
                        keyboard = set_lot_keyboard(update, lot)
                        reply_markup = InlineKeyboardMarkup(keyboard)

                        print_lot(update, context, lot, reply_markup)
                elif len(recent_lots) > 5:
                    recent_lots = recent_lots[len(recent_lots)-5:len(recent_lots)]
                    for lot in recent_lots:

                        # keyboard
                        keyboard = set_lot_keyboard(update, lot)
                        reply_markup = InlineKeyboardMarkup(keyboard)

                        print_lot(update, context, lot, reply_markup)
                else:
                    send_404_view_last(update, context)

        # create_lot
        def create_lot_button(update, context):
            query = update.callback_query
            if query.data == 'create_lot':

                # logics
                query.answer()
                query.edit_message_text(text='Continue...')

                # message
                send_image_message(update, context)

                # export context
                context.user_data['enable_create_lot'] = True
                context.user_data['enable_image'] = True

        # view_my_lots
        def view_my_lots_button(update, context):
            query = update.callback_query
            if query.data == 'view_my_lots':

                # logics
                query.answer()
                query.edit_message_text(text='Searching for your lots...')
                my_lots = Lot.objects.filter(user_id=update.effective_user.username)
                if len(my_lots) > 0:
                    for lot in my_lots:

                        # keyboard
                        keyboard = set_lot_keyboard(update, lot)
                        reply_markup = InlineKeyboardMarkup(keyboard)

                        print_lot(update, context, lot, reply_markup)
                else:
                    send_404_view_my(update, context)

        # view_my_bids
        def view_my_bids_button(update, context):
            query = update.callback_query
            if query.data == 'view_my_bids':

                # logics
                query.answer()
                query.edit_message_text(text='Looking for your bids...')
                create_user(update)
                user = CustomUser.objects.get(user_id=update.effective_user.id)
                my_bids = UserBid.objects.filter(user_id=user)
                if len(my_bids) > 0:
                    for bid in my_bids:
                        lot = bid.lot

                        # keyboard
                        keyboard = set_lot_keyboard(update, lot)
                        reply_markup = InlineKeyboardMarkup(keyboard)

                        print_lot(update, context, lot, reply_markup, bid)
                else:
                    send_404_view_bids(update, context)

        # delete_lot
        def delete_lot_button(update, context):
            query = update.callback_query
            if query.data[:10] == 'delete_lot':

                # logics
                query.answer()
                pk = int(query.data[11:])
                lot = Lot.objects.filter(pk=pk).first()
                if lot:
                    if default_storage.exists(lot.image_url):
                        default_storage.delete(lot.image_url)
                    lot.delete()
                    send_lot_deleted_message(update, context, pk)
                else:
                    send_404_delete_lot(update, context)

        # make_bid
        def make_bid_button(update, context):
            query = update.callback_query
            if query.data[:8] == 'make_bid':
                print('starting bid')

                # logics
                query.answer()

                pk = int(query.data[9:])
                lot = Lot.objects.filter(pk=pk).first()
                print('lot found:', lot)
                create_user(update)
                print('user created')

                if lot:
                    print('lot exists')
                    if lot.current_applicant != str(update.effective_user.username):
                        print('not applicant')
                        minimal_bid = find_min_bid(lot)
                        print('min bid', minimal_bid)
                        user = CustomUser.objects.get(user_id=update.effective_user.id)
                        print('user', user)
                        previous_bid = UserBid.objects.filter(user=user, lot=lot).first()
                        print('prev bid', previous_bid)
                        if previous_bid:
                            previous_bid.delete()
                        print('prev bid deleted')
                        print(CustomUser.objects.get(user_id=update.effective_user.id))
                        print(lot)
                        print(minimal_bid)

                        # UserBid saving
                        new_user_bid = UserBid(
                            user=CustomUser.objects.get(user_id=update.effective_user.id),
                            lot=lot,
                            bid_cost=minimal_bid+lot.current_price
                        )
                        print('new user bid created')
                        new_user_bid.save()
                        print('new user bid saved')

                        # Lot changing
                        lot.current_price += minimal_bid
                        lot.current_applicant = update.effective_user.username
                        lot.bidders.add(CustomUser.objects.get(user_id=update.effective_user.id))
                        lot.save()
                        print('lot saved')
                        send_success_bid(update, context)
                    else:
                        send_fail_bid(update, context)

        # refresh_lot
        def refresh_button(update, context):
            query = update.callback_query
            if query.data[:7] == 'refresh':

                # logics
                query.answer()
                pk = int(query.data[8:])
                lot = Lot.objects.filter(pk=pk).first()
                if lot:
                    # keyboard
                    keyboard = set_lot_keyboard(update, lot)
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    print_lot(update, context, lot, reply_markup)
                else:
                    send_404_refresh_lot(update, context)

        # search_lot
        def search_lot_button(update, context):
            query = update.callback_query
            if query.data == 'search_lot':

                # logics
                query.answer()
                query.edit_message_text(text='Continue...')

                # message
                send_search_message(update, context)

                # export content
                context.user_data['enable_search'] = True

    # Handles

        # image handle
        def handle_image(update, context):
            # user_id = update.effective_user.id
            if context.user_data['enable_image'] is True:

                # import context
                context.user_data['enable_image'] = False
                if update.message.photo and context.user_data['enable_create_lot'] is True:

                    # logics
                    photo = update.message.photo[-1]
                    file_id = photo.file_id
                    image_url = f'{settings.IMAGE_FOLDER}/{file_id}.jpg'

                    new_file = context.bot.get_file(file_id)

                    # message
                    send_description_message(update)

                    # export context
                    context.user_data['image_url'] = image_url
                    context.user_data['new_file'] = new_file
                    context.user_data['enable_description'] = True

                else:
                    context.user_data['enable_image'] = True

        # text handle
        def handle_text(update, context):

            # Searching lot

            # Get search data
            if context.user_data['enable_search'] is True:
                context.user_data['enable_search'] = False

                # logics
                search_data = update.message.text
                object_list = Lot.objects.filter(
                    Q(description__icontains=search_data)
                )
                if not object_list.exists():
                    send_404_search_lot(update)
                else:
                    for lot in object_list:
                        keyboard = set_lot_keyboard(update, lot)
                        reply_markup = InlineKeyboardMarkup(keyboard)

                        print_lot(update, context, lot, reply_markup)

            # Creating lot

            # Get description
            elif context.user_data['enable_description'] is True:
                context.user_data['enable_description'] = False

                # logics
                description = update.message.text

                # export context
                context.user_data['description'] = description

                # message
                send_price_message(update)
                context.user_data['enable_price'] = True

            # Get price
            elif context.user_data['enable_price'] is True:

                # logics
                try:
                    price = float(update.message.text)
                    if price > 0:

                        # export context
                        context.user_data['enable_price'] = False
                        context.user_data['price'] = price

                        # message
                        send_expiration_hours_message(update)
                        context.user_data['enable_expiration_hours'] = True
                    else:
                        send_price_error_message(update)

                except ValueError:
                    send_price_error_message(update)

            # Get expiration hours
            elif context.user_data['enable_expiration_hours'] is True:

                # logics
                try:
                    expiration_hours = int(update.message.text)
                    if 1 <= expiration_hours <= 24:

                        # export context
                        context.user_data['enable_expiration_hours'] = False
                        context.user_data['enable_create_lot'] = False

                        # import context
                        image_url = context.user_data['image_url']
                        description = context.user_data['description']
                        price = context.user_data['price']
            # Create new lot
                        new_lot = Lot(
                            user_id=update.effective_user.username, description=description, start_price=price,
                            image_url=image_url,
                            current_price=price, current_applicant='None', expiration_hours=expiration_hours
                        )
                        new_lot.save()

                        # download media
                        new_file = context.user_data['new_file']
                        new_file.download(custom_path=image_url)

                        # expire timer
                        def delete_lot(something):
                            lot = Lot.objects.filter(pk=new_lot.pk).first()
                            if lot.current_applicant != 'None':

                                # getting applicant id
                                last_user_bid = UserBid.objects.filter(bid_cost=lot.current_price).first()
                                applicant = CustomUser.objects.filter(user_id=last_user_bid.user.user_id).first()

                                send_purchase_message(context, applicant.user_id, lot)
                            send_expiration_message(update, lot)
                            if default_storage.exists(lot.image_url):
                                default_storage.delete(lot.image_url)
                            lot.delete()

                        context.job_queue.run_once(delete_lot, expiration_hours * 3600, context=update.effective_user.id)

                        # message
                        send_lot_created_message(update)

                        return context_menu(update, context)

                    else:
                        send_expiration_hours_error_message(update)
                # error message
                except ValueError:
                    send_expiration_hours_error_message(update)

# Dispatcher handlers

        # Commands
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("cancel", cancel_operation))
        dispatcher.add_handler(CommandHandler("help", bot_help))
        dispatcher.add_handler(CommandHandler("menu", context_menu))

        # Buttons
        dispatcher.add_handler(CallbackQueryHandler(create_lot_button, pattern='create_lot'))
        dispatcher.add_handler(CallbackQueryHandler(view_last_auctions_button, pattern='view_last'))
        dispatcher.add_handler(CallbackQueryHandler(view_my_lots_button, pattern='view_my_lots'))
        dispatcher.add_handler(CallbackQueryHandler(view_my_bids_button, pattern='view_my_bids'))
        dispatcher.add_handler(CallbackQueryHandler(delete_lot_button, pattern='delete_lot'))
        dispatcher.add_handler(CallbackQueryHandler(search_lot_button, pattern='search_lot'))
        dispatcher.add_handler(CallbackQueryHandler(make_bid_button, pattern='make_bid'))
        dispatcher.add_handler(CallbackQueryHandler(refresh_button, pattern='refresh'))

        # Logics
        dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

        # Polling
        updater.start_polling()
        updater.idle()

