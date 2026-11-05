import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("9112824032:AAHo2r7DzuVSVeQ_A_QCpVJ1ehU98dqBGi8")

BALANCE = {}
PRODUCTS = {
    "netflix": {"name": "Netflix 1 Month", "price": 199},
    "prime": {"name": "Prime Video 1 Month", "price": 149},
    "disney": {"name": "Disney+ Hotstar 1 Month", "price": 149},
    "spotify": {"name": "Spotify Premium 1 Month", "price": 99}
}

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🛍️ Shop", callback_data="shop")],
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile")],
        [InlineKeyboardButton("ℹ️ Seller Info", callback_data="seller")],
        [InlineKeyboardButton("📞 Support", callback_data="support")]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="home")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    BALANCE.setdefault(user.id, 1000)
    text = f"👋 Hello {user.first_name}!\n\nWelcome to Demo Shop Bot\n\nDemo Balance: 1000₹ দেওয়া আছে\nনিচে থেকে যেকোনো অপশন বেছে নাও 👇"
    if update.message:
        await update.message.reply_text(text, reply_markup=main_menu())
    else:
        await update.callback_query.edit_message_text(text, reply_markup=main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    BALANCE.setdefault(user.id, 1000)
    data = query.data

    if data == "home":
        await start(update, context)

    elif data == "shop":
        keyboard = []
        for key, p in PRODUCTS.items():
            keyboard.append([InlineKeyboardButton(f"{p['name']} - {p['price']}₹", callback_data=f"buy_{key}")])
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="home")])
        await query.edit_message_text("🛍️ **Shop**\n\nকিনতে চাইলে প্রোডাক্টে ক্লিক করো:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data.startswith("buy_"):
        key = data.replace("buy_", "")
        p = PRODUCTS[key]
        if BALANCE[user.id] >= p['price']:
            BALANCE[user.id] -= p['price']
            text = f"✅ Order Successful!\n\n📦 Product: {p['name']}\n💸 Price: {p['price']}₹\n💰 Remaining Balance: {BALANCE[user.id]}₹\n\nDemo Order - এটা আসল অর্ডার না।"
        else:
            text = f"❌ Balance কম আছে!\n\nতোমার Balance: {BALANCE[user.id]}₹\nলাগবে: {p['price']}₹"
        await query.edit_message_text(text, reply_markup=back_menu())

    elif data == "balance":
        await query.edit_message_text(f"💰 **Your Balance**\n\nBalance: {BALANCE[user.id]}₹\n\nDemo তে 1000₹ দেওয়া আছে।", reply_markup=back_menu(), parse_mode="Markdown")

    elif data == "profile":
        await query.edit_message_text(f"👤 **Profile**\n\nName: {user.first_name}\nID: {user.id}\nUsername: @{user.username}\nBalance: {BALANCE[user.id]}₹", reply_markup=back_menu(), parse_mode="Markdown")

    elif data == "seller":
        await query.edit_message_text("ℹ️ **Seller Info**\n\nShop Name: Demo Shop\nOwner: Asif\nStatus: Online ✅\n\nএটা Demo Bot", reply_markup=back_menu(), parse_mode="Markdown")

    elif data == "support":
        await query.edit_message_text("📞 **Support**\n\nযেকোনো সমস্যার জন্য @Asif কে মেসেজ করো।", reply_markup=back_menu(), parse_mode="Markdown")

def main():
    print("Bot Started...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
