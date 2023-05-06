from typing import Final
from telegram import Update, Chat,Message
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from joblib import load
import pandas as pd


data = []
contatore = 0

async def start(update:Update, context :ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao, sono il bot che ti aiuterà a scoprire il tuo livello di diabete!"+
                                    "\nIniziamo partendo dal sapere il tuo nome")

def selectKeyboard():
    keyboard = [[InlineKeyboardButton("SI", callback_data='SI'),
                    InlineKeyboardButton("NO", callback_data='NO')]]
    if contatore==3 or contatore==14 or contatore==15:
        keyboard = []
    elif contatore==13:
        keyboard = [[InlineKeyboardButton("1", callback_data='1'),
                    InlineKeyboardButton("2", callback_data='2'),
                    InlineKeyboardButton("3", callback_data='3'),
                    InlineKeyboardButton("4", callback_data='4'),
                    InlineKeyboardButton("5", callback_data='5')]]
    elif contatore==17:
        keyboard = [[InlineKeyboardButton("MASCHIO", callback_data='maschio'),
                    InlineKeyboardButton("FEMMINA", callback_data='femmina')]]
    elif contatore==18:
        keyboard=[
            [InlineKeyboardButton("1", callback_data='1'),
            InlineKeyboardButton("2", callback_data='2'),
            InlineKeyboardButton("3", callback_data='3'),
            InlineKeyboardButton("4", callback_data='4'),
            InlineKeyboardButton("5", callback_data='5'),
            InlineKeyboardButton("6", callback_data='6')],
            [InlineKeyboardButton("7", callback_data='7'),
            InlineKeyboardButton("8", callback_data='8'),
            InlineKeyboardButton("9", callback_data='9'),
            InlineKeyboardButton("10", callback_data='10'),
            InlineKeyboardButton("11", callback_data='11'),
            InlineKeyboardButton("12", callback_data='12'),
            InlineKeyboardButton("13", callback_data='13')]
            ]
    elif contatore==19:
        keyboard=[[InlineKeyboardButton("1", callback_data='1'),
            InlineKeyboardButton("2", callback_data='2'),
            InlineKeyboardButton("3", callback_data='3'),
            InlineKeyboardButton("4", callback_data='4'),
            InlineKeyboardButton("5", callback_data='5'),
            InlineKeyboardButton("6", callback_data='6')]]
    elif contatore==20:
        keyboard=[[InlineKeyboardButton("1", callback_data='1'),
            InlineKeyboardButton("2", callback_data='2'),
            InlineKeyboardButton("3", callback_data='3'),
            InlineKeyboardButton("4", callback_data='4'),
            InlineKeyboardButton("5", callback_data='5'),
            InlineKeyboardButton("6", callback_data='6'),
            InlineKeyboardButton("7", callback_data='7'),
            InlineKeyboardButton("8", callback_data='8')]]
    return keyboard

async def button(update:Update, context :ContextTypes.DEFAULT_TYPE):
    global contatore
    query = update.callback_query
    print(update.callback_query.message.text)
    await query.message.edit_text(query.message.text+" "+query.data)

    if(query.data=='maschio'):
        data.append(1.0)
        print("ho aggiunto 1")
        print(data)
    elif(query.data=='femmina'):
        data.append(0.0)
        print("ho aggiunto 0")
        print(data)
    elif(query.data=='SI'):
        data.append(1.0)
        print("ho aggiunto 0")
        print(data)
    elif(query.data=='NO'):
        data.append(0.0)
        print("ho aggiunto 0")
        print(data)
    else:
        data.append(float(query.data))
        print("ho aggiunto"+query.data)
        print(data)

    contatore+=1
    if contatore<21:
        keyboard = selectKeyboard()
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(question(), reply_markup=reply_markup)
    else:
        model = load('DecTree.joblib')
        df = buildDF()
        predict = model.predict(df)
        print(predict[0])
        response = ""
        if(predict[0]==0.0):
            response = "non diabetico"
        elif(predict[0]==1.0):
            response="prediabetico"
        else:
            response="diabetico"
        await update.callback_query.message.reply_text("Prevedo che sei un soggetto "+response)


async def ready(update:Update, context :ContextTypes.DEFAULT_TYPE):
    global contatore
    domanda = question()
    print(domanda)
    keyboard = selectKeyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(domanda, reply_markup=reply_markup)
    print("ok sono arrivato qua")
    print(data)

def errore():
    global contatore
    contatore = 0

def responseGeneral(text:str) -> str:
    global contatore
    if(text=="Alessandro Favaro"):
        return "Ok, "+text+" per cominciare l'intero processo digita /sonoPronto"
    
    elif(contatore==3 or contatore==14 or contatore==15):
        try:
            number = float(text)
            check = True
            if(contatore==14):
                if(number<1 or number>30):
                    check = False
            elif(contatore==15):
                if(number<1 or number>30):
                    check = False
            
            if(check):
                data.append(number)
                contatore = contatore+1
                return(question())
            else:
                return("risposta non corretta,prova ad inserire un numero valido ")
        except:
            return("Risposta sbagliata, prova ad inserire un numero corretto")
    
    else:
        return("non ho capito mi dispiace")
        errore()



async def responseBot(update:Update, context :ContextTypes.DEFAULT_TYPE):
    messageType: str = update.message.chat.type
    text = update.message.text
    print (f'User({update.message.chat.id}) in {messageType}:{text}') 

    response = responseGeneral(text)
    await ready(update, ContextTypes.DEFAULT_TYPE)
     
#async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

     #query = update.callback_query
     #await query.answer()
     #await query.edit_message_text(text=f"Seledddd:{query.data}")

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery

def question():
    questions = ["Sei un soggetto iperteso?",
                 "Soffri di colesterolo alto?",
                 "Hai eseguito controlli sul colesterolo negli ultimi 5 anni?",
                 "Qual è il tuo BMI?",
                 "Sei un fumatore? (almeno 100 sigarette nella tua vita)",
                 "Hai mai fatto un infarto?",
                 "Soffri di problemi cardiaci?",
                 "Hai svolto attività fisica negli ultimi 30 giorni? ",
                 "Consumi regolarmente frutta? (almeno 1 frutto al giorno)",
                 "Consumi regolarmente verdura? (almeno 1 frutto al giorno)",
                 "Consumi spesso alcol? (almeno 14 drinks a settimana, per l'uomo; almeno 7 drinks per le donne)",
                 "Hai altre patoligie regresse?",
                 "Hai visto un dottore negli ultimi 12 mesi?",
                 "Indica il tuo indice di salute generale:\n1 --> eccellente\n2 --> molto buono\n3 --> buono\n4 --> normale\n5 --> scarso",
                 "Quanti giorni negli ultimi 30 la tua salute mentale non è stata buona?",
                 "Quanti giorni negli ultimi 30 la tua salute psicologica non è stata buona?",
                 "Hai difficoltà nel camminare o nel fare le scale?",
                 "Sei maschio o femmina?",
                 "Quanti anni hai? (indicare l'indice della categoria presa da _AGEG5YR)",
                 "Indica il tuo livello di istruzione:\n1 --> Mai andato a scuola \n2 --> Scuola elementare\n3 --> Licenza media\n4 --> Diplomato\n5 --> Laurea triennale\n6 --> Laurea magistrale",
                 "Indica il tuo livello di entrate economiche (indicare l'indice della categoria presa da INCOME2)"]
    
    return questions[contatore]
   
def buildDF():
    df = pd.DataFrame({
    'Iperteso':[data[0]],
    'Colesterolo':data[1],
    'ControlloColesterolo':data[2],
    'BMI':data[3],
    'Fumatore':data[4],
    'Infarto':data[5],
    'ProblemiCardiaci':data[6],
    'AttivitàFisica':data[7],
    'Fruits':data[8],
    'Veggies':data[9],
    'ConsumoAlcol':data[10],
    'AnyHealthcare':data[11],
    'NoDocbcCost':data[12],
    'SaluteGenerale':data[13],
    'SaluteMentale':data[14],
    'SaluteFisica':data[15],
    'DifficolàSportiva':data[16],
    'Sex':data[17],
    'Age':data[18],
    'Education':data[19],
    'Income':data[20]
    })
    return df
    

print ('inizio bot')
app = Application.builder().token("6242272055:AAHe6DjncVtpP8CuJhTWl9iIccMfoj4QIr0").build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('sonoPronto', ready))
app.add_handler(MessageHandler(filters.TEXT, responseBot))
app.add_handler(CallbackQueryHandler(button))
print ('polling...')
app.run_polling(poll_interval=3)
