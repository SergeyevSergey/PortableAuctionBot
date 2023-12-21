from telegram import InlineKeyboardButton
from .functions import find_min_bid

# Menu keyboard
menu_keyboard = [
    [InlineKeyboardButton("🕔 View last auctions", callback_data='view_last')],
    [InlineKeyboardButton("🔍 Search auctions", callback_data='search_lot')],
    [InlineKeyboardButton("🆕 Create new lot", callback_data='create_lot')],
    [InlineKeyboardButton("📈 View my lots", callback_data='view_my_lots')],
    [InlineKeyboardButton("💰 View my bids", callback_data='view_my_bids')],
]


# Lot keyboard
def set_lot_keyboard(update, lot):
    print('- set_lot_keyboard function activated')
    if lot.user_id == update.effective_user.username:
        keyboard = [[InlineKeyboardButton("❌ Delete", callback_data=f'delete_lot_{lot.pk}')]]
        print('     set delete button')
    else:
        if lot.current_applicant != update.effective_user.username:
            keyboard = [[InlineKeyboardButton(f"💸 Make a bid:    +{find_min_bid(lot)} UZS", callback_data=f'make_bid_{lot.pk}')]]
            print('     set bid button')
        else:
            keyboard = [[InlineKeyboardButton(f"🔄 Refresh", callback_data=f'refresh_{lot.pk}')]]
            print('     set refresh button')

    return keyboard
