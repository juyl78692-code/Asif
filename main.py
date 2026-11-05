import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("9112824032:AAGGm_aLoDFiYUeVrGJEXLu6I9IM8OvXwjU")

# Demo data - pore tumi bodlate parbe
BALANCE = {}
PRODUCTS = {
    "netflix": {"name": "Netflix 1 Month", "price": 250},
    "prime": {"name": "Prime Video 1 Month", "price": 180},
    "disney": {"name": "Disney+ 1 Month", "price": 220},
}

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🛍️ Shop", callback_data="shop"),
         InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile"),
         InlineKeyboardButton("ℹ️ Seller Info", callback_data="seller")],
        [InlineKeyboardButton("📞 Support", callback_data="support")],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="back")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    BALANCE.setdefault(user.id, 0)
    text = (
        f"👋 Welcome {user.first_name}!\n\n"
        f"🛒 **MD ASIF SELH SHOP**\n"
        f"Trusted Digital Shop in Bangladesh\n\n"
        f"Niche theke jeta dorkar select koro:"
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=main_menu(), parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=main_menu(), parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    BALANCE.setdefault(user.id, 0)
    data = query.data

    if data == "back":
        await start(update, context)
        return

    if data == "shop":
        text = "🛍️ **SHOP**\n\nKinte chao konta select koro:"
        keyboard = []
        for key, p in PRODUCTS.items():
            keyboard.append([InlineKeyboardButton(f"{p['name']} - {p['price']} TK", callback_data=f"buy_{key}")])
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back")])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data.startswith("buy_"):
        key = data.replace("buy_", "")
        p = PRODUCTS[key]
        if BALANCE[user.id] >= p['price']:
            BALANCE[user.id] -= p['price']
            await query.edit_message_text(f"✅ Order Done!\n\n{p['name']} kinecho.\nBaki Balance: {BALANCE[user.id]} TK", reply_markup=back_menu())
        else:
            await query.edit_message_text(f"❌ Balance kom!\n\nDorkar: {p['price']} TK\nTomar ache: {BALANCE[user.id]} TK\n\nAge Balance add koro.", reply_markup=back_menu())

    elif data == "balance":
        await query.edit_message_text(f"💰 **Your Balance**\n\nBalance: {BALANCE[user.id]} TK\n\nBalance add korte Support e msg dao.", reply_markup=back_menu(), parse_mode="Markdown")

    elif data == "profile":
        await query.edit_message_text(f"👤 **Profile**\n\nName: {user.first_name}\nID: {user.id}\nBalance: {BALANCE[user.id]} TK", reply_markup=back_menu(), parse_mode="Markdown")

    elif data == "seller":
        await query.edit_message_text("ℹ️ **Seller Info**\n\nShop: MD ASIF SELH SHOP\nOwner: MD Asif\nTrusted Seller ✅\nDelivery: Instant", reply_markup=back_menu(), parse_mode="Markdown")

    elif data == "support":
        await query.edit_message_text("📞 **Support**\n\nKono problem hole ekhane msg dao:\n@MD_ASIF_SELL", reply_markup=back_menu(), parse_mode="Markdown")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot Started...")
    app.run_polling()
