import os, requests, json

currentDirectory = os.path.dirname(os.path.realpath(__file__))
response = requests.get('https://api.kawalcorona.com/indonesia/provinsi/')
list = response.json()
final_d = []
msg = ""
for data in list:

   ## data corona ##
   kode_provi = data['attributes']['Kode_Provi']
   provinsi = data['attributes']['Provinsi']
   kasus_posi = data['attributes']['Kasus_Posi']
   kasus_semb = data['attributes']['Kasus_Semb']
   kasus_meni = data['attributes']['Kasus_Meni']

   ## put togather as array##
   data_array = str(provinsi)+","+str(kasus_posi)+","+str(kasus_semb)+","+str(kasus_meni)
   try:
      f = open(currentDirectory+"/tmp/"+str(kode_provi),"r")
      f.close()
      print(str(kode_provi)+" exists")
   except IOError:
      f = open(currentDirectory+"/tmp/"+str(kode_provi),"w")
      f.write(data_array)
      f.close()
      print(str(kode_provi)+" created")

   ## read from array file ##
   f = open(currentDirectory+"/tmp/"+str(kode_provi),"r")
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
      f = open(currentDirectory+"/tmp/"+str(kode_provi),"w")
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
   group_id = []
   remove_id = []

   ## get active group ID ##
   response = requests.get('https://api.telegram.org/bot1264034596:AAEzvf_ShnwYYkENitzGllz-ZzMmWfWRg80/getUpdates')
   list = response.json()
   for group in list['result']:
      id = group['message']['chat']['id']
      group_id.append(id)
   uniq = set(group_id)
   d_val = []
   for x in uniq:
      d_val.append(x)
   try:
      f = open(currentDirectory+"/tmp/group","r")
      exists_array = json.loads(f.read())
      merge = exists_array+d_val
      uniq = set(merge)
      d_val = []
      for x in uniq:
         d_val.append(x)
      f = open(currentDirectory+"/tmp/group","w")
      f.write(str(d_val))
      f.close()
   except IOError:
      f = open(currentDirectory+"/tmp/group","w")
      f.write(str(d_val))
      f.close()
   f = open(currentDirectory+"/tmp/group","r")
   json_group = json.loads(f.read())
   print json_group

   ## send to active group ##
   for g_id in json_group:
      response = requests.get('https://api.telegram.org/bot1264034596:AAEzvf_ShnwYYkENitzGllz-ZzMmWfWRg80/sendMessage?chat_id='+str(g_id)+'&parse_mode=HTML&disable_web_page_preview=false&text='+telegram_notif)
      if response.status_code == 200:
         print "berhasil "+str(g_id)
      elif response.status_code == 403 or response.status_code == 400:
         print "error "+str(g_id)
         remove_id.append(g_id)
   for trim in remove_id:
      json_group.remove(trim)
   f = open(currentDirectory+"/tmp/group","w")
   f.write(str(json_group))
   f.close()
