from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "9112824032:AAGGm_aLoDFiYUeVrGJEXLu6I9IM8OvXwjU"
URL = "https://t.me/suvosk7869"

CART = chr(0x1F6D2)
MONEY = chr(0x1F4B0)
USER = chr(0x1F464)
CHART = chr(0x1F4CA)
CROWN = chr(0x1F451)
FIRE = chr(0x1F525)
TICK = chr(0x2705)
CHAT = chr(0x1F4AC)
STAR = chr(0x2B50)
WAVE = chr(0x1F44B)
GLOBE = chr(0x1F310)
SPARK = chr(0x2728)
ROCKET = chr(0x1F680)
LOCK = chr(0x1F512)
BELL = chr(0x1F514)
DIAMOND = chr(0x1F48E)
HEART = chr(0x2764)
CROSS = chr(0x274C)
INFO = chr(0x2139)
SHOP = chr(0x1F3EA)

USER_BAL = {}

def get_bal(uid):
    if uid not in USER_BAL:
        USER_BAL[uid] = 0
    return USER_BAL[uid]

def home_text_en(uid, nm):
    bal = get_bal(uid)
    txt = CART + " " + SPARK + " MD ASIF SELH SHOP " + SPARK + " " + CART + "\n\n"
    txt += WAVE + " Welcome " + nm + "! " + HEART + "\n\n"
    txt += STAR + " STORE HIGHLIGHTS " + STAR + "\n"
    txt += DIAMOND + " Premium Keys\n"
    txt += ROCKET + " Instant Delivery\n"
    txt += LOCK + " Secure Payment\n\n"
    txt += "ID: " + uid + " " + TICK + "\n"
    txt += MONEY + " Balance: Rs."+str(bal)+" " + MONEY + "\n\n"
    txt += TICK + " Tap Shop Now! " + FIRE
    return txt

def home_buttons_en():
    b1 = InlineKeyboardButton(CART+" Shop", callback_data="shop_en")
    b2 = InlineKeyboardButton(MONEY+" Balance", callback_data="bal1_en")
    b3 = InlineKeyboardButton(USER+" Profile", callback_data="prof_en")
    b4 = InlineKeyboardButton(CHART+" History", callback_data="hist_en")
    b5 = InlineKeyboardButton(INFO+" Seller Info", callback_data="seller_en")
    b6 = InlineKeyboardButton(GLOBE+" Language", callback_data="lang_en")
    b7 = InlineKeyboardButton(CHAT+" "+CROWN+" SUPPORT - CONTACT OWNER "+CROWN+" "+CHAT, url=URL)
    return InlineKeyboardMarkup([[b1,b2],[b3,b4],[b5,b6],[b7]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    nm = u.first_name
    uid = str(u.id)
    txt = home_text_en(uid, nm)
    m = home_buttons_en()
    await update.message.reply_text(txt, reply_markup=m)

async def all_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data
    u = q.from_user
    nm = u.first_name
    uid = str(u.id)
    uname = u.username or "No Username"
    bal = get_bal(uid)

    if d == "set_en":
        txt = home_text_en(uid, nm)
        await q.edit_message_text(txt, reply_markup=home_buttons_en())
        return

    if d.startswith("lang"):
        b1 = InlineKeyboardButton("English US", callback_data="set_en")
        b2 = InlineKeyboardButton("Bangla", callback_data="set_en")
        mk = InlineKeyboardMarkup([[b1],[b2]])
        try:
            await q.edit_message_text(GLOBE+" Choose Your Language "+GLOBE, reply_markup=mk)
        except:
            pass
        return

    if d.startswith("shop"):
        txt = CART+" "+SPARK+" SHOP - PANEL LIST "+SPARK+"\n\n"+DIAMOND+" Select Your Panel:"
        a1 = InlineKeyboardButton(FIRE+" ALASTOR V4 - 99 "+FIRE, callback_data="p1_en")
        a2 = InlineKeyboardButton(STAR+" CONQUEROR - 199 "+STAR, callback_data="p2_en")
        a3 = InlineKeyboardButton(DIAMOND+" LORD PANEL - 349 "+DIAMOND, callback_data="p3_en")
        a4 = InlineKeyboardButton(CROWN+" OWNER PANEL - 999 "+CROWN, callback_data="p4_en")
        a5 = InlineKeyboardButton(TICK+" Back", callback_data="home_en")
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([[a1],[a2],[a3],[a4],[a5]]))
        return

    if d.startswith("p1") or d.startswith("p2") or d.startswith("p3") or d.startswith("p4"):
        txt = FIRE+" Panel Selected! "+FIRE+"\n\n"+SPARK+" Click Add Balance to buy"
        a1 = InlineKeyboardButton(MONEY+" Add Balance", callback_data="bal1_en")
        a2 = InlineKeyboardButton("Back", callback_data="shop_en")
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([[a1],[a2]]))
        return

    if d.startswith("bal1"):
        txt = MONEY+" "+SPARK+" ADD BALANCE PAGE "+SPARK+"\n\nID: "+uid+"\n"+MONEY+" Balance: Rs."+str(bal)+"\n\n"+BELL+" Click Add Balance button to add balance "+BELL
        a1 = InlineKeyboardButton(MONEY+" "+DIAMOND+" Add Balance "+DIAMOND, callback_data="bal2_en")
        a2 = InlineKeyboardButton("Back", callback_data="home_en")
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([[a1],[a2]]))
        return

    if d.startswith("bal2"):
        txt = CROWN+" "+SPARK+" OWNER PAYMENT "+SPARK+"\n\n"+CROWN+" MD ASIF SEKH "+CROWN+"\n"+CHAT+" @suvosk7869\n"+HEART+" HAM MUSLIM "+HEART+"\n\n"+ROCKET+" Message to add balance "+ROCKET
        a1 = InlineKeyboardButton(CROWN+" "+SPARK+" Message Owner "+SPARK, url=URL)
        a2 = InlineKeyboardButton("Back", callback_data="bal1_en")
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([[a1],[a2]]))
        return

    if d.startswith("prof"):
        txt = USER+" "+SPARK+" MY PROFILE "+SPARK+"\n\n"+WAVE+" Welcome "+nm+"! "+HEART+"\n\n"+STAR+" Name: "+nm+"\n"+LOCK+" Chat ID: "+uid+"\n"+GLOBE+" Username: @"+uname+"\n"+MONEY+" Balance: Rs."+str(bal)
        a1 = InlineKeyboardButton("Back", callback_data="home_en")
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([[a1]]))
        return

    if d.startswith("hist"):
        txt = CHART+" "+SPARK+" PURCHASE HISTORY "+SPARK+"\n\n"+CROSS+" No Purchased Key "+CROSS+"\n\n"+BELL+" You have not purchased any key yet!"
        a1 = InlineKeyboardButton(CART+" Go To Shop", callback_data="shop_en")
        a2 = InlineKeyboardButton(TICK+" Back", callback_data="home_en")
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([[a1],[a2]]))
        return

    if d.startswith("seller"):
        txt = SHOP+" "+SPARK+" SELLER INFORMATION "+SPARK+" "+SHOP+"\n\n"
        txt += CROWN+" Owner Name: MD ASIF SEKH "+CROWN+"\n\n"
        txt += CHAT+" Username: @suvosk7869\n"
        txt += STAR+" Shop: MD ASIF SELH SHOP\n"
        txt += DIAMOND+" Premium Keys Seller\n"
        txt += ROCKET+" Instant Delivery\n"
        txt += LOCK+" Trusted Seller\n"
        txt += HEART+" HAM MUSLIM "+HEART+"\n\n"
        txt += TICK+" 100% Trusted & Secure "+TICK+"\n"
        txt += BELL+" Contact For Any Help "+BELL
        a1 = InlineKeyboardButton(CHAT+" "+CROWN+" Message Owner "+CROWN+" "+CHAT, url=URL)
        a2 = InlineKeyboardButton(TICK+" Back", callback_data="home_en")
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([[a1],[a2]]))
        return

    if d.startswith("home"):
        txt = home_text_en(uid, nm)
        await q.edit_message_text(txt, reply_markup=home_buttons_en())
        return

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(all_buttons))
print("READY SELLER INFO + BORO SUPPORT")
app.run_polling()
