import requests

response = requests.get('https://api.kawalcorona.com/indonesia/provinsi/')
list = response.json()
final_d = []
msg = ""
for data in list:
   kode_provi = data['attributes']['Kode_Provi']
   ## data corona ##
   provinsi = data['attributes']['Provinsi']
   kasus_posi = data['attributes']['Kasus_Posi']
   kasus_semb = data['attributes']['Kasus_Semb']
   kasus_meni = data['attributes']['Kasus_Meni']
   ## put togather as array##
   data_array = str(provinsi)+","+str(kasus_posi)+","+str(kasus_semb)+","+str(kasus_meni)
   try:
      f = open("/project/corona_api/tmp/"+str(kode_provi),"r")
      f.close()
      print(str(kode_provi)+" exists")
   except IOError:
      f = open("/project/corona_api/tmp/"+str(kode_provi),"w")
      f.write(data_array)
      f.close()
      print(str(kode_provi)+" created")

   ## read from array file ##
   f = open("/project/corona_api/tmp/"+str(kode_provi),"r")
   f_array = f.read().split(",")
   f_posi = f_array[1]
   f_semb = f_array[2]
   f_meni = f_array[3]

   ## check per array ##
   if f_posi != str(kasus_posi) or f_semb != str(kasus_semb) or f_meni != str(kasus_meni):

      val_posi = int(kasus_posi) - int(f_posi)
      if val_posi > 0:
         val_posi = " ( naik "+str(val_posi)+" angka )"
      else:
         val_posi = ""

      val_semb = int(kasus_semb) - int(f_semb)
      if val_semb > 0:
         val_semb = " ( naik "+str(val_semb)+" angka )"
      else:
         val_semb = ""

      val_meni = int(kasus_meni) - int(f_meni)
      if val_meni > 0:
         val_meni = " ( naik "+str(val_meni)+" angka )"
      else:
         val_meni = ""

      data_file = str(provinsi)+"|"+"<b>"+str(kasus_posi)+"</b>"+str(val_posi)+"|"+"<b>"+str(kasus_semb)+"</b>"+str(val_semb)+"|"+"<b>"+str(kasus_meni)+"</b>"+str(val_meni)
      final_d.append(data_file)

      ## update data ##
      f = open("/project/corona_api/tmp/"+str(kode_provi),"w")
      f.write(data_array)
      f.close()
      print(str(kode_provi)+" update")

if not final_d:
   print('no changes')
else:
   for notif in final_d:
      split = notif.split("|")
      msg += "<b>[ "+split[0]+" ]</b>%0A"
      msg += "Positif "+split[1]+"%0A"
      msg += "Sembuh "+split[2]+"%0A"
      msg += "Meninggal "+split[3]+"%0A%0A"

   ## all indonesia statistic ##

   response = requests.get('https://api.kawalcorona.com/indonesia/')
   list = response.json()

   ## start messgae vars ##

   data_idn = "<b>[ Seluruh Indonesia ]</b>%0A"
   data_idn += "Positif <b>"+list[0]['positif']+"</b>%0A"
   data_idn += "Sembuh <b>"+list[0]['sembuh']+"</b>%0A"
   data_idn += "Meninggal <b>"+list[0]['meninggal']+"</b>%0A%0A"

   link = "<a href='https://www.detik.com/tag/virus-corona'>Cek lebih lanjut..</a>"
   title = "<b>KawalCoronaIndonesia</b>%0A%0A"

   telegram_notif = title+msg+data_idn+link

   ## end message vars ##

   ## send to telegram ##
   requests.get('https://api.telegram.org/bot1264034596:AAEzvf_ShnwYYkENitzGllz-ZzMmWfWRg80/sendMessage?chat_id=-231890212&parse_mode=HTML&disable_web_page_preview=false&text='+telegram_notif)