### COVID19 BOT ###
### Sample Bot '1264034596:AAEzvf_ShnwYYkENitzGllz-ZzMmWfWRg80' ###

import os, requests, json

currentDirectory = os.path.dirname(os.path.realpath(__file__))
list_result = str()
response = requests.get('https://api.kawalcorona.com/indonesia/provinsi/')
list = response.json()

def open_file():
   f = open(currentDirectory+"/data","r")
   f_data = f.read()
   f.close()
   return f_data

try:
   open_file()
except IOError:
   with open(currentDirectory+'/data', 'w') as outfile:
      json.dump(list, outfile)
   open_file()

file_data = json.loads(open_file())

def returnNotMatches(a, b):
    return [[x for x in a if x not in b], [x for x in b if x not in a]]

result = returnNotMatches(list,file_data)

## comapre array ##
if result[0] == result[1]:
   print "[ no changes ]"
else:
   for x,y in zip(result[0],result[1]):
      provinsi = "%0A<b>[ "+str(x['attributes']['Provinsi'])+" ]</b>%0A"
      x_kasus_posi = x['attributes']['Kasus_Posi']
      x_kasus_semb = x['attributes']['Kasus_Semb']
      x_kasus_meni = x['attributes']['Kasus_Meni']

      y_kasus_posi = y['attributes']['Kasus_Posi']
      y_kasus_semb = y['attributes']['Kasus_Semb']
      y_kasus_meni = y['attributes']['Kasus_Meni']

      if x_kasus_posi != y_kasus_posi:
         val = x_kasus_posi-y_kasus_posi
         msg_kasus_posi = "Positif <b>"+str(x_kasus_posi)+"</b> ( naik "+str(val)+" angka )%0A"
      else:
         msg_kasus_posi = "Positif <b>"+str(x_kasus_posi)+"</b>%0A"
      if x_kasus_semb != y_kasus_semb:
         val = x_kasus_semb-y_kasus_semb
         msg_kasus_semb = "Sembuh <b>"+str(x_kasus_semb)+"</b> ( naik "+str(val)+" angka )%0A"
      else:
         msg_kasus_semb = "Sembuh <b>"+str(x_kasus_semb)+"</b>%0A"
      if x_kasus_meni != y_kasus_meni:
         val = x_kasus_meni-y_kasus_meni
         msg_kasus_meni = "Meninggal <b>"+str(x_kasus_meni)+"</b> ( naik "+str(val)+" angka ) %0A"
      else:
         msg_kasus_meni = "Meninggal <b>"+str(x_kasus_meni)+"</b>%0A"

      list_result += provinsi+msg_kasus_posi+msg_kasus_semb+msg_kasus_meni

   with open(currentDirectory+'/data', 'w') as outfile:
      json.dump(list, outfile)

   ## all indonesia statistic ##
   response = requests.get('https://api.kawalcorona.com/indonesia/')
   list_idn = response.json()

   ## start message's vars ##
   data_idn = "%0A<b>[ Seluruh Indonesia ]</b>%0A"
   data_idn += "Positif <b>"+list_idn[0]['positif']+"</b>%0A"
   data_idn += "Sembuh <b>"+list_idn[0]['sembuh']+"</b>%0A"
   data_idn += "Meninggal <b>"+list_idn[0]['meninggal']+"</b>%0A%0A"

   link = "<a href='https://www.detik.com/tag/virus-corona'>Cek lebih lanjut..</a>"
   title = "<b>KawalCoronaIndonesia</b>%0A"

   telegram_notif = title+list_result+data_idn+link

   ## send to telegram in active ID ##
   group_id = []
   remove_id = []
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
      f = open(currentDirectory+"/group","r")
      exists_array = json.loads(f.read())
      merge = exists_array+d_val

      uniq = set(merge)
      d_val = []
      for x in uniq:
         d_val.append(x)
      ## store data to 'group' file ##
      f = open(currentDirectory+"/group","w")
      f.write(str(d_val))
      f.close()
   except IOError:
      f = open(currentDirectory+"/group","w")
      f.write(str(d_val))
      f.close()

   f = open(currentDirectory+"/group","r")
   json_group = json.loads(f.read())
   print "Sending..\n"
   for g_id in json_group:
      response = requests.get('https://api.telegram.org/bot1264034596:AAEzvf_ShnwYYkENitzGllz-ZzMmWfWRg80/sendMessage?chat_id='+str(g_id)+'&parse_mode=HTML&disable_web_page_preview=false&text='+telegram_notif)
      if response.status_code == 200:
         print "[ "+str(g_id)+" ] Success.."
      elif response.status_code == 403 or response.status_code == 400:
         print "[ "+str(g_id)+" ] Fail !"
         ## remove failure group_id from array ##
         remove_id.append(g_id)

   for trim in remove_id:
      json_group.remove(trim)

   ## store active group_id to group file ##
   f = open(currentDirectory+"/group","w")
   f.write(str(json_group))
   f.close()
