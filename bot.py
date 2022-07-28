from pyrogram import Client
from pyrogram.types import Message
from moodle import delete
import random
from config import *

#created by anonedev
bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

users = {}

proxysall = {}
		
def crypt_char(char):
    map = '@./=#$%&:,;_-|0123456789abcd3fghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    i = 0
    for ch in map:
        if ch == char:
            return map[len(map) - 1 - i]
        i+=1
    return char

def proxydec(text):
    i = 0
    decryptText = ''
    while i < len(text):
        decryptText += crypt_char(text[i])
        i+=2
    return decryptText

@bot.on_message()
async def messages_control(c: Client, m: Message):
	usern = m.from_user.username
	msg = m.text
	
	if msg is None:
		msg = ''
	
	if msg == '/start':
		await m.reply('👋Hola '+usern+'😁\nSea bienvenido a DeleteTGBot simple y rapido con este bot podras eliminar los archivos que has subido a tu nube☁ reenviandole a este bot un enlace o un txt👍')
	
	if '/help' in msg:
		mssg = 'Como usar el bot:\n\nAsegurarse de que el enlace o txt a enviar al bot sea exactamente el que te da el bot con el cual subes a la nube\n\nAsegurarse de que las credenciales, es decir usuario, contraseña y host sean correctos\n\nEste es un ejemplo👇\n\n/auth usuario contraseña https://direccion.de.nube\n\nPuede añadir proxy para nubes que lo requieran\n\nEste es un ejemplo👇\n\n/proxy socks5://SGWBDLWBSLEBWNWLWIWBENM2WJKQWNWKWN2JWJ\n\nNota:Una vez configure usuario, contraseña y host de una nube y solo quiere borrar de esa nube no debe configurarla mas hasta que el bot se reinicie\n\nRespecto al proxy si se lo pones y este deja de funcionar puedes quitarlo usando /off'
		await m.reply(mssg)
			
	if msg.startswith('/auth'):
		splitmsg = msg.split(' ')
		users[usern] = {'user':splitmsg[1],'passw':splitmsg[2],'host':splitmsg[3]}
		await m.reply('Se guardaron las credenciales✅')
		
	if msg.startswith('/proxy'):
		proxysplit = msg.split(' ')[1]
		proxy_token = proxydec(proxysplit.split('://')[1]).split(':')
		ip = proxy_token[0]
		port = int(proxy_token[1])
		proxy_final = dict(https=f'socks5://{ip}:{port}', http=f'socks5://{ip}:{port}')
		proxysall[usern] = proxy_final
		await m.reply('Proxy guardado✅')
		
	if '/off' in msg:
		del proxysall[usern]
		await m.reply('Se quito el proxy👍')
		
	if msg.startswith('https') or msg.startswith('http'):
		urls = m.text
		urlsfix = m.text
		
		proxy = None
		if proxysall != {}:
			proxy = proxysall[usern]
		
		if '?token=' in urls:
			token = urls.split('=')[1]
			urlsfix = urls.replace(f'?token={token}','')
			
		if users == {}:
			await m.reply('Credenciales sin guardar💢')
		else:
			msgcheck = await m.reply("⏳Comprobando autorización...\n")
			
			userdatat = users[usern]
			ret = delete(userdatat['user'],userdatat['passw'],userdatat['host'],urlsfix,proxy)
			
			if 'melogee' in ret:
				await msgcheck.edit("Credenciales correctas✅")
				if 'borre' in ret:
					await msgcheck.edit(f"ENLACE eliminado exitosamente de la nube✅\n\nLogeate y compruebalo👇\n{urls}")
			else:
				await msgcheck.edit("Credenciales incorrectas❌")
	
	if m.document:
		proxy = None
		if proxysall != {}:
			proxy = proxysall[usern]
			
		if users == {}:
			await m.reply('Credenciales sin guardar💢')
		else:
			txt = await c.download_media(m.document)
			msgcheck = await m.reply('⌛Comprobando autorización...')
				
			userdatat = users[usern]
			with open(txt, 'r') as txtfile:
				txtlines = txtfile.read().split('\n')
				
				delurls = 0
				for line in txtlines:
					linefix = line
					
					if '?token=' in line:
						token = line.split('=')[1]
						linefix = line.replace(f'?token={token}','')
						
					ret = delete(userdatat['user'],userdatat['passw'],userdatat['host'],linefix,proxy)
					
					if 'melogee' in ret:
						try:
							await msgcheck.edit("Credenciales correctas✅")
						except:
							pass
						
						if 'borre' in ret:
							delurls+= 1
							try:
								await msgcheck.edit(f"Borrando {delurls} urls de la nube...☁")
							except:
								pass
							
							if len(txtlines) == delurls:
								await msgcheck.edit('TXT eliminado de la nube exitosamente✅\nAutor👨‍💻: @anonedev')
								break
					else:
						await msgcheck.edit("Credenciales incorrectas❌")
						break
					
if __name__ == "__main__":
	print("Bot iniciado")
	bot.run()