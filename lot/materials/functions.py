from lot.models import CustomUser


# Restrictions
def place_restrictions(context):
    context.user_data['enable_create_lot'] = False
    context.user_data['enable_image'] = False
    context.user_data['enable_description'] = False
    context.user_data['enable_price'] = False
    context.user_data['enable_expiration_hours'] = False
    context.user_data['enable_search'] = False


# Create user
def create_user(update):
    user = CustomUser.objects.filter(user_id=update.effective_user.id).first()
    if user:
        pass
    else:
        new_user = CustomUser(user_id=update.effective_user.id)
        new_user.save()


# Find minimal bid
def find_min_bid(lot):
    start_price = lot.start_price
    if 0 < start_price < 500000:
        minimal_bid = (lot.start_price/100)*15
    elif 500000 <= start_price < 1000000:
        minimal_bid = (lot.start_price/100)*10
    elif 1000000 <= start_price < 10000000:
        minimal_bid = (lot.start_price/100)*6
    elif 10000000 <= start_price < 25000000:
        minimal_bid = (lot.start_price/100)*3
    elif 25000000 <= start_price < 100000000:
        minimal_bid = (lot.start_price/100)*1.5
    else:
        minimal_bid = (lot.start_price/100)

    return round(minimal_bid, 2)
