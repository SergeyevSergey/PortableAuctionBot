from django.core.files.storage import default_storage


# -- Warnings

def send_expiration_message(update, lot):
    if lot.current_applicant != 'None':
        update.message.reply_text(f"❗️Attention❗\n\nYour lot {lot.description} has been expired!\n\nThe buyer is: @{lot.current_applicant}\nCurrent price: {lot.current_price} UZS\n\nPlease, contact your buyer to make a deal.")
    else:
        update.message.reply_text(f"❗️Attention❗\n\nYour lot {lot.description} has been expired!\n\nUnfortunately, nobody made any bids for this lot.")


def send_purchase_message(context, username, lot):
    context.bot.send_message(
        chat_id=username,
        text=f"❗️Attention❗\n\nyou are the winner of the {lot.description} auction with your bid!\n\nLot keeper: @{lot.user_id}\nCurrent price: {lot.current_price} UZS\n\nPlease, contact your lot keeper to make a purchase."
    )


# -- Messages


# create lot message
def send_image_message(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please send me an image for the lot.\nP.S - I will receive only first image that you send"
    )


def send_description_message(update):
    update.message.reply_text("Now, please provide a description for the lot.")


def send_price_message(update):
    update.message.reply_text(
        "Now, please provide a start price in UZS for your product, enter number.\nExample: 5000.00"
    )


def send_price_error_message(update):
    update.message.reply_text(
        "Please, enter number greater than zero."
    )


def send_expiration_hours_message(update):
    update.message.reply_text(
        "Got it! At the last, please, provide a expiration hours for the lot, enter number of hours that your lot will be exist.\n(from 1 to 24)"
    )


def send_expiration_hours_error_message(update):
    update.message.reply_text(
        "Enter integer number between 1 and 24."
    )


# search lot message
def send_search_message(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Please, enter description of something that you want to find:'
    )


# lot created
def send_lot_created_message(update):
    update.message.reply_text("Lot has been created successfully!")


# lot deleted
def send_lot_deleted_message(update, context, pk):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Lot with id {pk} has been deleted!'
    )

# -- Commands


# /start command
def send_welcome(update, user_name, reply_markup):
    update.message.reply_text(
        f'Hello {user_name}, our dear user! Welcome to the PortableAuction bot! Here you can create your own auction and make a bid.\n\n❗❗️❗️️Attention❗️❗️❗️\nNotice that maximum expiration time of every lot is 24 hours!\n\nPlease, choose one option below:',
        reply_markup=reply_markup
    )


# /menu command
def send_menu(update, reply_markup):
    update.message.reply_text(
        f'Anything else I could help you with?',
        reply_markup=reply_markup
    )


# /help command
def send_help(update):
    print('send help started')
    update.message.reply_text("I'm here to help you!\n\n/start - Start bot\n/menu - Open the menu\n/cancel - Cancel current operation")


# /cancel command
def send_cancel(update):
    update.message.reply_text(
        "Operation canceled."
    )


# -- Buttons


# view last auctions (404 message)
def send_404_view_last(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Unfortunately, there are no lots yet."
    )


# view my auctions (404 message)
def send_404_view_my(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You have not created any lot yet."
    )


# view my bids (404 message)
def send_404_view_bids(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You have not bid any lot yet."
    )


# delete lot (404 message)
def send_404_delete_lot(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Lot not found!'
    )


# refresh lot (404 message)
def send_404_refresh_lot(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Not found!'
    )


# search lot (404 message)
def send_404_search_lot(update):
    update.message.reply_text('Nothing found')


# bid lot (success)
def send_success_bid(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Your bid has been saved!'
    )


# bid lot (fail)
def send_fail_bid(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'You are already current applicant!'
    )


# -- Prints


# Print lot
def print_lot(update, context, lot, reply_markup, bid=None):
    if default_storage.exists(lot.image_url):
        if bid is None:
            caption = f'Description:\n{lot.description}\n\nStart price: {lot.start_price} UZS\nCurrent price: {lot.current_price} UZS\nCurrent applicant: @{lot.current_applicant}\n\nLot created by: @{lot.user_id}'
        else:
            if lot.current_applicant != update.effective_user.username:
                caption = f'Description:\n{lot.description}\n\nStart price: {lot.start_price} UZS\nCurrent price: {lot.current_price} UZS\nCurrent applicant: @{lot.current_applicant}\n\nYour bid was: {bid.bid_cost} UZS\n\nLot created by: @{lot.user_id}'
            else:
                caption = f'Description:\n{lot.description}\n\nStart price: {lot.start_price} UZS\nCurrent price: {lot.current_price} UZS\nCurrent applicant: @{lot.current_applicant}\n\nLot created by: @{lot.user_id}'

        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open(lot.image_url, 'rb'),
            caption=caption,
            reply_markup=reply_markup
        )
    else:
        update.message.reply_text(
            "Error 404. Lot not found!"
        )

