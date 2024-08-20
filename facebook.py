
from email.mime.text import MIMEText
import os
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import time
import re
import pickle
import random
import numpy as np
from selenium.webdriver.chrome.service import Service as ChromeService
from seleniumbase import Driver

def scriptFB2():

    

    # Máximo número de intentos de reinicio
    max_retries = 3
    retry_delay = 5  # segundos

    #variables follow/unfollow
    siguiendo = 0
    num_unfollow = 0

    #index reset hastag
    hashtagHecho = 0
    nexthashtag = 0
    todoHashtag = False

    # Nombre del archivo para almacenar el índice
    indice_filename = "guardaIndice_FB_EN.txt"
    indice_filename_tema = "guardaTema_FB_EN.txt"
    cookies_file = "cookiesFacebookEN.pkl"

    while True:
        """
        try:
             # Ruta al ejecutable de ChromeDriver
            chromedriver_path = 'C:/Users/sandr/Desktop/chromedriver.exe'

            # Configurar opciones de Chrome
            chrome_options = Options()

            # Adding argument to disable the AutomationControlled flag
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")

            # Exclude the collection of enable-automation switches
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

            # Turn-off userAutomationExtension
            chrome_options.add_experimental_option("useAutomationExtension", False)

            # Deshabilitar el pop-up de guardar contraseña
            prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
            chrome_options.add_experimental_option("prefs", prefs)

            # Desactivar notificaciones
            chrome_options.add_argument("--disable-notifications")

            # Inicializar el servicio de ChromeDriver
            service = ChromeService(executable_path=chromedriver_path)

            # Iniciar el navegador Chrome con las opciones configuradas
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            pass
        """
        driver = Driver(uc=True)

        # Registra el tiempo de inicio
        inicio_programa = datetime.now()

        # Lee el índice desde el archivo si existe, de lo contrario, asigna el valor inicial
        if os.path.exists(indice_filename_tema):
            with open(indice_filename_tema, "r") as file:
                # Lee el contenido del archivo y verifica si está vacío antes de convertirlo a entero
                indice_str = file.read().strip()
                max_retries = int(indice_str) if indice_str else 3
                print(f"imprime dentro TEMA cogido!!!!!!!!! {max_retries}")
        else:
            max_retries = 3

        if max_retries == 1:
            from hashtagsFB_EN3 import hashtags
            from hashtagsFB_EN3 import TemaHastags
            from comentariosFB_EN3 import comentarios
            
        elif max_retries == 2:
            from hashtagsFB_EN2 import hashtags
            from hashtagsFB_EN2 import TemaHastags
            from comentariosFB_EN2 import comentarios
            
        elif max_retries == 3:
            
            from hashtagsFB_EN1 import hashtags
            from hashtagsFB_EN1 import TemaHastags
            from comentariosFB_EN1 import comentarios

        # random per el time sleeep
        wait = random.randint(5, 14)

        #variable tiempo para comentario
        tiempo_inicial_comment = time.time()
        num_comentario = 0
        #variable tiempo para like
        tiempo_inicial_like = time.time()
        num_like = 0
        #variable tiempo para like
        tiempo_inicial_likeComment = time.time()
        num_likeComment = 0

        numHashtag = len(hashtags)
        #numHashtag = 0
        indice = 0

        
        unfollow_realizados = 0
        index = 0
        topePost = 150

        commentReels = 0
        commentPost = 0
        daleLike = 0
        hover_count = 0


        try:
            # URL de la página web
            url = 'https://www.facebook.com/'
            driver.get(url)
            time.sleep(5)

            #ENVIAR MAIL ERROR funcion 1
            def enviar_correo(error_message):
                # Configuración del servidor SMTP
                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                email_user = "*******+m"
                email_pass = "trgh bpjy ufgh gbnc"

                # Crear el mensaje de correo electrónico con el mensaje de error
                subject = "¡¡¡FB ENGLISH Reiniciar bot!!"
                body = f"Atento:\n\n{error_message}"
                message = MIMEText(body, 'plain', 'utf-8')
                message["Subject"] = subject
                message["From"] = email_user
                message["To"] = "newsplaygroup@gmail.com"

                try:
                    # Configurar la conexión SMTP
                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    server.login(email_user, email_pass)
                    server.sendmail(email_user, ["newsplaygroup@gmail.com"], message.as_string())
                    print("------------ ¡¡Correo electrónico ERROR enviado con éxito!! -------------------")
                except smtplib.SMTPException as e:
                    print(f"Error al enviar el correo electrónico: {str(e)}")

            #ENVIAR MAIL BIEN /CORRECTO funcion 2
            def enviar_correo_correcto(bien_message):
                # Configuración del servidor SMTP
                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                email_user = "myprueba365@gmail.com"
                email_pass = "trgh bpjy ufgh gbnc"

                # Crear el mensaje de correo electrónico con el mensaje de error
                subject = "FB ENGLISH PROCESO TERMINADO CORRECTAMENTE"
                body = f"Datos: \n\n{bien_message}"
                message = MIMEText(body, 'plain', 'utf-8')
                message["Subject"] = subject
                message["From"] = email_user
                message["To"] = "newsplaygroup@gmail.com"

                try:
                    # Configurar la conexión SMTP
                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    server.login(email_user, email_pass)
                    server.sendmail(email_user, ["newsplaygroup@gmail.com"], message.as_string())
                    print("------------ ¡¡Correo electrónico Proceso correcto enviado con éxito!! -------------------")
                except smtplib.SMTPException as e:
                    print(f"Error al enviar el correo electrónico correcto: {str(e)}")

              

            #clic aviso cookies
            try:
                cookies = driver.find_element(By.XPATH,'//button[contains(text(), "Permitir todas las cookies")]')
                cookies.click()
                print("clic cookies ok!!")
                time.sleep(5)
            except Exception as e:
                print(f"No se pudo hacer clic en 'cookies': {e}")

   

            try:
                # login facebook
                userName = "Mario Pello"
                userId = "61555234327598"
                errorCookie = False
                if os.path.getsize(cookies_file) > 0:
                    try:
                        cookies = pickle.load(open(cookies_file, "rb"))
                        for cookie in cookies:
                            driver.add_cookie(cookie)
                        driver.refresh()
                        print(f"BIEN BIEN desde for cookies!!!")
                    except Exception as e:
                        errorCookie = True
                        time.sleep(wait)
                        print(f"****mierda no cookie*****")
                if os.path.getsize(cookies_file) == 0 or errorCookie == True:
                    user_input = driver.find_element(By.XPATH,"//input[@id='email']")
                    user_input.send_keys("newsplaygroup@gmail.com")
                    time.sleep(2)
                    passwd_input = driver.find_element(By.XPATH,"//input[@id='pass']")
                    passwd_input.send_keys("Elmarques9")
                    time.sleep(2)
                    login = driver.find_element(By.XPATH,"//button[@name='login']")
                    login.click()
                    time.sleep(10)
                    print("Te has registrado con exito!! ")
                    try:
                        time.sleep(10)
                        pickle.dump( driver.get_cookies() , open(cookies_file,"wb"))
                        print("BIEN HE LEIDO cookies!!!!!")
                    except Exception as e:
                        print("*No he podido copiar cookies!!!!!")

                # Lee el índice desde el archivo si existe, de lo contrario, asigna el valor inicial
                if os.path.exists(indice_filename):
                    with open(indice_filename, "r") as file:
                        # Lee el contenido del archivo y verifica si está vacío antes de convertirlo a entero
                        indice_str = file.read().strip()
                        ind = int(indice_str) if indice_str else 0
                        print(f"imprime dentro texto cogido!!!!!!!!! {indice}")
                else:
                    ind = 0          

                for indice in range(ind, ind + numHashtag):
                    #buscar hashtag
                    try:
                        time.sleep(wait)
                        selected_hashtag = hashtags[indice]
                        time.sleep(wait)
                        commentArea = driver.find_element(By.XPATH,"//input[@aria-label='Search Facebook']")
                        commentArea.send_keys(Keys.CONTROL + "a")
                        time.sleep(2)
                        # Presiona la tecla "Backspace" para borrar el texto seleccionado
                        commentArea.send_keys(Keys.BACKSPACE)        
                        commentArea.send_keys(f"#{selected_hashtag}")
                        time.sleep(wait)
                        commentArea.send_keys(Keys.ENTER)
                        
                        time.sleep(3)
                        driver.find_element(By.XPATH,"//div[@aria-label='Exit typeahead']").click()
                        print("imput hashtag dentro!!")
                        time.sleep(wait)

                    except Exception as e:
                        time.sleep(wait)
                        selected_hashtag = hashtags[indice]
                        search_url_hastag = f'https://www.facebook.com/hashtag/{selected_hashtag}'
                        driver.get(search_url_hastag)

                    
                    

                    for index in range(topePost):
                        print(f"index: {index}")
                        #random acciones 1=megusta 2=comment 3=like comment
                        accion = random.randint(0, 1)
                        darSeguir = random.randint(0, 3)
                        #accion = 8
                        #print(accion)
                        time.sleep(wait)

                        

                        try:
                            try:
                                allow_cookies_button = driver.find_elements(By.XPATH, '//span[contains(text(), "Permitir todas las cookies")]')
                                if allow_cookies_button:
                                    # Hacer clic en el botón
                                    allow_cookies_button[1].click()
                                    print("Se hizo clic en 'Permitir todas las cookies'.")
                                    time.sleep(10)
                            except Exception as e:
                                pass
                            try:
                                try:
                                    driver.find_element(By.XPATH,"//div[@aria-label='Cerrar']").click()
                                except Exception as e:
                                    pass

                                try:
                                    userId = "61555234327598"
                                    user_input = driver.find_element(By.XPATH,"//input[@name='email']")
                                    user_input.send_keys("newsplaygroup@gmail.com")
                                    time.sleep(2)
                                    passwd_input = driver.find_element(By.XPATH,"//input[@name='pass']")
                                    passwd_input.send_keys("Elmarques9")
                                    time.sleep(2)
                                    
                                    try:
                                        driver.find_element(By.XPATH,"//*[@aria-label='Accessible login button']").click()
                                    except Exception as e:
                                        pass
                                    
                                    time.sleep(10)
                                except Exception as e:
                                    pass
                            except Exception as e:
                                pass 
                        except Exception as e:
                            pass

                        try:
                            notFound = driver.find_element(By.XPATH, '//span[contains(text(), "No hemos encontrado resultados")]')
                            if notFound:
                                time.sleep(2)
                                print(f">>>>> no exite hastag break <<<<<<")
                                break
                        except Exception as e:
                            pass
                        try:
                            notFound = driver.find_element(By.XPATH, '//span[contains(text(), "Este contenido no está disponible en este momento")]')
                            if notFound:
                                time.sleep(2)
                                print(f">>>>> no exite hastag break <<<<<<")
                                break
                        except Exception as e:
                            pass

                        try:
                            time.sleep(5)
                            numPubli = WebDriverWait(driver, 10).until(
                                EC.presence_of_all_elements_located((By.XPATH, '//*[@aria-label="Acciones para esta publicación"]'))
                            )
                            totalPubli = len(numPubli)
                            print(f"...............total publi: {totalPubli} ")
                            if index == totalPubli:
                                print(f" num MAXIMO PUBLICACIONES  Índice {index} es igual al número de elementos encontrados {totalPubli} BREAK.")
                                break
                        except Exception as e:
                            pass

                        if accion == 0:
                            # Verifica la condición de tiempo y número de likes max 100 en 1hora
                            tiempo_actual_like = time.time()
                            if tiempo_actual_like - tiempo_inicial_like >= 38 or num_like == 0:
                                
                                meGusta = driver.find_elements(By.XPATH,"//div[@aria-label='Me gusta']")
                                elementosTotales = len(meGusta)
                                print(f"elementos me gusta: {elementosTotales} index: {index} num like: {num_like}")
                                
                                try:
                                    # Haz clic en el elemento elegido
                                    meGusta[index].click()
                                    daleLike += 1
                                    num_like += 1
                                    print(f"clic num like: ---> {num_like}")
                                except NoSuchElementException as e:
                                    meGusta[daleLike].click()
                                    daleLike += 1
                                    num_like += 1
                                    print(f"clic dale like count: ---> {num_like}")
                                except Exception as e:
                                    print(f"******Error array like****")

                                time.sleep(wait)               

                                # Actualiza el tiempo inicial para el próximo minuto
                                tiempo_inicial_like = time.time()
                                time.sleep(3)
                            else:
                                print(f"Tiempo insuficiente para realizar like Espera!!!!!")

                        if accion == 1:
                            tiempo_actual_comment = time.time()
                            # Compara si ha pasado un minuto desde el tiempo inicial
                            if tiempo_actual_comment - tiempo_inicial_comment >= 60 or num_comentario == 0:
                                #btn clic comentario
                                time.sleep(wait)
                                comment_elements = driver.find_elements(By.XPATH,"//*[@aria-label='Comentar']")
                                elementosTotales = len(comment_elements)
                                print(f"elementos COMMENT 1111: {elementosTotales} index: {index} comment reeels {commentReels}")

                                comment_elements2 = driver.find_elements(By.XPATH, "//*[@aria-label='Dejar un comentario']")
                                elementosTotales2 = len(comment_elements2)
                                print(f"elementos COMMENT 22222: {elementosTotales2} index: {index} comment post: {commentPost}")

                                # Click on the first visible element
                                if commentReels <= elementosTotales:
                                    try:
                                        try:
                                            comment_elements[commentReels].click()
                                            commentReels += 1
                                        except Exception as e:
                                            comment_elements[index].click()
                                            commentReels += 1
                                            print("****No esta elements 1111****")

                                        try:

                                            time.sleep(wait)
                                            commentYo = driver.find_elements(By.XPATH,f'//div[contains(@aria-label,"Comentario de {userName}")]')
                                            print(f"coment-> {len(commentYo)} username-> {userName}")
                                            if len(commentYo) == 0:
                                                #elige comentario del array
                                                comentario_aleatorio = random.choice(comentarios)
                                                time.sleep(wait)

                                                print("dentro comentario")
                                                comment = driver.find_element(By.XPATH,'//*[@aria-label="Escribe algo…"]')
                                                #comment = driver.find_element(By.XPATH,'//div[contains(text(), "Escribe algo…")]')
                                                print("dentro comentario2")
                                                comment.send_keys(comentario_aleatorio)
                                                print("dentro comentario3")
                                                time.sleep(wait)
                                                # div aria-label="Comentar"
                                                #driver.find_element(By.ID, "focused-state-composer-submit").click()
                                                print("dentro comentario4")
                                                #driver.find_element(By.,'//div[@aria-label="Escribe algo…"]')
                                                comment.send_keys(Keys.ENTER)
                                                print("dentro comentario1")
                                                time.sleep(wait)

                                                try:
                                                    cerrare = driver.find_elements(By.XPATH,"//div[@aria-label='Cerrar']")
                                                    cerrare[1].click()
                                                    time.sleep(5)
                                                except Exception as e:
                                                    print("***Error cerrar post comentario 111***")

                                                try:
                                                    cerrare = driver.find_elements(By.XPATH,"//div[@aria-label='Cerrar']")
                                                    cerrare[2].click()
                                                    time.sleep(5)
                                                except Exception as e:
                                                    print("***Error cerrar post comentario 222***")
                                                
                                                
                                                num_comentario += 1
                                                print(f"----------> COMENT Echo {num_comentario}")
                                                time.sleep(wait)
                                            else:
                                                print("****estaaaaaaaa COMMENT REPE REPE REPE 111")
                                        except Exception as e:
                                            print("***Error escribir comentario ***")

                                        #aviso FB demasiados comments
                                        try:
                                            btnSeguir3 = driver.find_element(By.XPATH,'//span[contains(text(), "Aceptar")]')
                                            btnSeguir3.click()
                                            print("Aceptar boton")
                                            time.sleep(wait)
                                        except Exception as e:
                                            print("xxxxx ERROR ACEPTAR BOTON 3333 xxxxxx")
                                        try:
                                            closed = driver.find_elements(By.XPATH,"//div[@aria-label='Cerrar']")
                                            closed[2].click()
                                            print("***BIEN closee warning***")
                                            time.sleep(5)
                                        except Exception as e:
                                            print("***Error closee warning***")

                                        if darSeguir == 3:
                                            try:
                                                clicSeguir = driver.find_elements(By.XPATH,'//div[contains(text(), "Seguir")]')
                                                followClick2 = len(clicSeguir)
                                                followClick = int(followClick2)
                                                followClick -= 1
                                                clicSeguir[followClick].click()            
                                                siguiendo += 1
                                                print(f"¡¡¡clic seguir user: {siguiendo} !!!")
                                                time.sleep(wait)
                                            except Exception as e:
                                                print("***Error clic seguir user***")   
                                                
                                    except Exception as e:
                                        print("Error clic boton comentario11111111")
                                    

                                    try:
                                        driver.find_element(By.XPATH,"//div[@aria-label='Cerrar']").click()
                                        time.sleep(5)
                                    except Exception as e:
                                        print("***Error cerrar post comentario 111***")
                                    time.sleep(45)
                                # Click on the first visible element
                                print(f" ---AVANS--- coment post: {commentPost} elementos totales: {elementosTotales2}")
                                if commentPost <= elementosTotales2:
                                    try:
                                        try:
                                            comment_elements2[commentPost].click()
                                            commentPost += 1
                                        except Exception as e:
                                            comment_elements2[index].click()
                                            commentPost += 1
                                            print("****No esta elements 2****")
                                        try:
                                            time.sleep(wait)
                                            commentYo = driver.find_elements(By.XPATH,f'//div[contains(@aria-label,"Comentario de {userName}")]')
                                            print(f"coment post-> {len(commentYo)} username-> {userName}")
                                            if len(commentYo) == 0:
                                                #elige comentario del array
                                                comentario_aleatorio = random.choice(comentarios)
                                                time.sleep(wait)

                                                print("dentro comentario")
                                                comment = driver.find_element(By.XPATH,'//*[@aria-label="Escribe algo…"]')
                                                #comment = driver.find_element(By.XPATH,'//div[contains(text(), "Escribe algo…")]')
                                                print("dentro comentario2")
                                                comment.send_keys(comentario_aleatorio)
                                                print("dentro comentario3")
                                                time.sleep(wait)
                                                # div aria-label="Comentar"
                                                #driver.find_element(By.ID, "focused-state-composer-submit").click()
                                                print("dentro comentario4")
                                                #driver.find_element(By.,'//div[@aria-label="Escribe algo…"]')
                                                comment.send_keys(Keys.ENTER)
                                                print("dentro comentario1")
                                                time.sleep(wait)
                                                
                                                num_comentario += 1
                                                print(f"----------> COMENT Echo {num_comentario}")
                                                time.sleep(wait)
                                                try:
                                                    popUP = driver.find_element(By.XPATH,'//span[contains(text(), "Revisión de la participación")]')
                                                    closede = driver.find_elements(By.XPATH,"//div[@aria-label='Cerrar']")
                                                    closede[2].click()
                                                except Exception as e:
                                                    print("salirrrrr")
                                            else:
                                                print("****estaaaaaaaa COMMENT REPE REPE REPE 222")

                                        except Exception as e:
                                            try:
                                                time.sleep(wait)
                                                commentYo = driver.find_elements(By.XPATH,f'//div[contains(@aria-label,"Comentario de {userName}")]')
                                                if len(commentYo) == 0:
                                                    #elige comentario del array
                                                    comentario_aleatorio = random.choice(comentarios)
                                                    time.sleep(wait)

                                                    print("2222dentro comentario")
                                                    comment = driver.find_element(By.XPATH,'//*[@aria-label="Escribe un comentario público…"]')
                                                    print("222dentro comentario2")
                                                    comment.send_keys(comentario_aleatorio)
                                                    print("2222dentro comentario3")
                                                    time.sleep(wait)
                                                    comment.send_keys(Keys.ENTER)
                                                    #enviar = driver.find_element(By.ID, "focused-state-composer-submit")
                                                    #enviar.click()
                                                    time.sleep(wait)
                                                    
                                                    num_comentario += 1
                                                    print(f"----------> COMENT Echo {num_comentario}")
                                                    time.sleep(wait)
                                                else:
                                                    print("****estaaaaaaaa COMMENT REPE REPE REPE post 3333")
                                                
                                            except Exception as e:
                                                try:
                                                    time.sleep(wait)
                                                    commentYo = driver.find_elements(By.XPATH,f'//div[contains(@aria-label,"Comentario de {userName}")]')
                                                    if len(commentYo) == 0:
                                                        #elige comentario del array
                                                        comentario_aleatorio = random.choice(comentarios)
                                                        time.sleep(wait)

                                                        print("2222dentro comentario")
                                                        comment = driver.find_element(By.XPATH,'//*[@aria-label="Envía tu primer comentario..."]')
                                                        print("222dentro comentario2")
                                                        comment.send_keys(comentario_aleatorio)
                                                        print("2222dentro comentario3")
                                                        time.sleep(wait)
                                                        comment.send_keys(Keys.ENTER)
                                                        #enviar = driver.find_element(By.ID, "focused-state-composer-submit")
                                                        #enviar.click()
                                                        time.sleep(wait)
                                                        
                                                        num_comentario += 1
                                                        print(f"----------> COMENT Echo {num_comentario}")
                                                        time.sleep(wait)

                                                        try:
                                                            popUP = driver.find_element(By.XPATH,'//span[contains(text(), "Revisión de la participación")]')
                                                            closede = driver.find_elements(By.XPATH,"//div[@aria-label='Cerrar']")
                                                            closede[2].click()
                                                        except Exception as e:
                                                            print("salirrrrr")
                                                    else:
                                                        print("****estaaaaaaaa COMMENT REPE REPE REPE post44444")
                                                                                                
                                                except Exception as e:
                                                    print("Ninguno funciona")
                                        try:
                                            time.sleep(wait)
                                            btnSeguir3 = driver.find_element(By.XPATH,'//span[contains(text(), "Aceptar")]')
                                            btnSeguir3.click()
                                            print("Aceptar boton")
                                        except Exception as e:
                                            pass
                                        try:
                                            time.sleep(wait)
                                            driver.find_element(By.XPATH,'//*[@aria-label="Aceptar"]').click()
                                            print("Aceptar boton")
                                        except Exception as e:
                                            print("xxxxx ERROR ACEPTAR BOTON 1111 xxxxxx")

                                    except Exception as e:
                                        print("Error clic boton comentario2222222222222")

                                    try:
                                        driver.find_element(By.XPATH,"//div[@aria-label='Salir de la página']").click()
                                        print("--- cerrar Post---")   
                                        time.sleep(5)
                                    except Exception as e:
                                        print("***Error cerrar post comentario salir***")  

                                    try:
                                        closed = driver.find_elements(By.XPATH,"//div[@aria-label='Cerrar']")
                                        closed[1].click()
                                        print("--- cerrar 1---") 
                                        time.sleep(5)
                                    except NoSuchElementException as e:
                                        closed = driver.find_element(By.XPATH,"//div[@aria-label='Cerrar']")
                                        closed.click()
                                        print("--- cerrar 2---")   
                                        time.sleep(5)
                                    except Exception as e:
                                        print("***Error cerrar post comentario 222***")  

                                # Actualiza el tiempo inicial para el próximo minuto
                                tiempo_inicial_comment = time.time()
                                time.sleep(3)
                
                            else:
                                print(f"Tiempo insuficiente para realizar comentario Espera!!!!!")
                            

                        if index == topePost - 1:
                            print(f"Tope post break")
                            break
                        else:
                            """
                            # Ejecutar un script de JavaScript para desplazar la barra de desplazamiento hacia abajo       
                            script = "window.scrollBy(0, 570);"
                            driver.execute_script(script)
                            time.sleep(wait)
                            """
                    #contar indice array hashtag
                    hashtagHecho += 1
                    fini = numHashtag - 1
                    if indice < fini:                        
                        nexthashtag = indice + 1
                        print(f"---> indice: {indice} numhastaag: {fini} HASTAG HECHOO: {hashtagHecho}")
                        todoHashtag = True
                    elif indice == fini:
                        todoHashtag = False
                        print(f" ELSE IFFFFFFFFFFFFFFF---> indice: {indice} numhastaag: {fini} HASTAG HECHOO: {hashtagHecho}")


                    time.sleep(5)
                    
                print(f"------------------------------¡He realizado todos los hashtag de la lista {TemaHastags} hastags totales: {indice}!-----------------------------------------")
                #indiceSend = indice + 1
                bien_message = f'¡He realizado todos los hashtag tema {TemaHastags} hastags totales: {indice} !'
                enviar_correo_correcto(bien_message)
                #empieza unfollow    

                try:
                    time.sleep(wait)
                    try:
                        driver.find_element(By.XPATH,"//*[@class='x3ajldb']").click()
                        print("--- click tu perfil---") 
                        time.sleep(wait)
                    except Exception as e:
                        try:
                            driver.find_element(By.XPATH,"//*[@aria-label='Tu perfil']").click()
                            print("--- click tu perfil---") 
                            time.sleep(wait)
                        except Exception as e:
                            print("***Error btn clic MAS perfil***")

                    try:
                        driver.find_element(By.XPATH,f'//a[@href="/me/"]').click()
                        time.sleep(wait)
                    except Exception as e:
                        print("***Error btn clic user perfil***")

                    try:
                        driver.find_element(By.XPATH,"//div[@aria-label='Ver recomendaciones']").click()
                        time.sleep(3)
                    except Exception as e:
                        print("***Error btn clic ver recomendaciones perfil***")

                    try:    
                        driver.find_element(By.XPATH,f'//a[@href="https://www.facebook.com/profile.php?id={userId}&sk=friends"]').click()
                        time.sleep(wait)

                        elemento_seguidos = driver.find_element(By.XPATH,'//span[contains(text(), "Seguidos")]') 

                        # Realiza un scroll hasta el elemento utilizando JavaScript
                        driver.execute_script("arguments[0].scrollIntoView();", elemento_seguidos)

                        scroll_offset = -100  # Ajusta este valor según tus necesidades

                        # Realiza un desplazamiento adicional hacia arriba (en este caso)
                        driver.execute_script(f"window.scrollBy(0, {scroll_offset});")
                    except Exception as e:
                        print("***Error btn clic amigos perfil + scroll***")

                    try:
                        time.sleep(wait)
                        driver.find_element(By.XPATH,f'//a[@href="https://www.facebook.com/profile.php?id={userId}&sk=following"]').click()
                        print("----clic seguidos correcto!!!")
                        time.sleep(wait)
                    except Exception as e:
                        pass

                    try:
                        # Encontrar todos los elementos div con las clases específicas
                        #elementos_div2 = driver.find_elements(By.XPATH, '//div[@class="x1iyjqo2 x1pi30zi"]')
                        elementos_div2 = driver.find_elements(By.XPATH, '//span[@class="x1lq5wgf xgqcy7u x30kzoy x9jhf4c xl1xv1r x1ey2m1c xlg9a9y x9f619 xds687c x10l6tqk x17qophe x13vifvy"]')
                        porcentaje_a_seleccionar = 0.5
                        total_elementos = len(elementos_div2)
                        numero_a_seleccionar = int(porcentaje_a_seleccionar * total_elementos)

                        # Seleccionar solo el 90% de los elementos
                        elementos_seleccionados = elementos_div2[:numero_a_seleccionar]
                        print(f"-----------------> Elementos seleccionados {numero_a_seleccionar}")
                    except Exception as e:
                        print("***Error btn amigos hover seleccionar***")

                    try:
                        # Realizar un hover en cada elemento  Vista previa del enlace  a aria-label="Suscribirse"
                        for elementoy in elementos_div2:
                            try:
                                # Utilizar ActionChains para realizar un hover
                                acciones1 = ActionChains(driver)
                                acciones1.move_to_element(elementoy).perform()
                                hover_count += 1
                                print(f" hover: {hover_count}")
                                time.sleep(25)
                            except Exception as e:
                                print("***Error hover foto perfil***")  

                            try:
                                driver.find_element(By.XPATH,"//div[@aria-label='Siguiendo']").click()
                                print(f"Seguiendo clic")
                                time.sleep(wait)
                            except NoSuchElementException as e:
                                driver.find_element(By.XPATH,'//span[contains(text(), "Siguiendo")]').click()
                                print(f"Seguiendo clic 2")
                                time.sleep(wait)
                            except Exception as e:
                                print("***Error clic siguiendo***")  

                            try:
                                driver.find_element(By.XPATH,'//span[contains(text(), "Dejar de seguir")]').click()
                                print(f"unfollow")
                                num_unfollow += 1
                                time.sleep(wait)
                            except Exception as e:
                                print("***Error clic dejar de seguir***")  
                            try:
                                driver.find_element(By.XPATH,"//div[@aria-label='Actualizar']").click()
                                print(f"Guardar")
                                time.sleep(wait)
                            except Exception as e:
                                pass
                            try:
                                time.sleep(2)
                                # Mover el ratón fuera del elemento para quitar el hover
                                acciones1.move_to_element_with_offset(elementoy, 0, 0).perform()
                            except Exception as e:
                                pass

                            # Verificar si se ha alcanzado el límite de 75 hover
                            if hover_count >= 75 or hover_count >= numero_a_seleccionar:
                                bien_message = f'FB ENGLISH unfollow {numero_a_seleccionar} usuarios ¡Ha terminado correctamente! '
                                enviar_correo_correcto(bien_message)
                                print("---------Se han alcanzado el tope hover. Deteniendo la ejecución.---------------")
                                break

                    except Exception as e:
                        print("***Error loop unfollow***")
                        
                except Exception as e:
                    print("***Error Processo unfollow***")

            except Exception as e:
                print("***Error LOGIN***")

            time.sleep(100)
            driver.quit()
        # Verificar si la ventana del programa está abierta
            
        except WebDriverException as e:
            print("************************************Se produjo un error crítico:*************************************************")
            print(f"{e}")
            print("**************************************Fin error crítico**************************************************")
            error_message = f'Se produjo un error crítico{e}'
            enviar_correo(error_message) 

        if 'driver' in locals():
                driver.quit()

        # Esperar un tiempo antes de intentar reiniciar
        time.sleep(retry_delay)

        # Registra el tiempo de finalización
        fin_programa = datetime.now()
        # Formatea las fechas en un formato legible
        formato_fecha_hora = "%d/%m/%Y %H:%M:%S"
        fecha_inicio_formateada = inicio_programa.strftime(formato_fecha_hora)
        fecha_fin_formateada = fin_programa.strftime(formato_fecha_hora)

        total_tiempo_programa2 = fin_programa - inicio_programa 
        total_tiempo_programa = total_tiempo_programa2

        if todoHashtag == True:
                # Guarda el índice actual en el archivo
            with open(indice_filename, "w") as file:               
                file.write(str(nexthashtag))
                print(f"--CONTINUANDO HASTAG despUes driver quit--------------{nexthashtag}")
            with open(indice_filename_tema, "w") as file:               
                file.write(str(max_retries))
                print(f"--write NEXT HASHTAG SEGUIRRR--------------{max_retries}")
                print(f"--tema hashtags:{TemaHastags} num hashtags totales: {numHashtag}")
                error_message = f'-- FB ENGLISH A MEDIAS HASHTAG = tema hashtags:{TemaHastags} num hashtags totales: {numHashtag}'
                enviar_correo_correcto(error_message)
            todoHashtag = False
        else:
            if max_retries == 3:
                indiceMail = indice + 1
                print(f"Seguir: {siguiendo}, Unfollow: {num_unfollow}, Like: {num_like}, Comentario: {num_comentario}, Like Comentario: {num_likeComment} número hashtags: {indiceMail} \ntiempo que ha tardado programa: {total_tiempo_programa} \nfecha inicio: {fecha_inicio_formateada} fecha fin: {fecha_fin_formateada}")
                bien_message = f'FB ENGLISH El programa ha realizado las siguientes operaciones \n\n Seguir: {siguiendo}, Unfollow: {num_unfollow}, Like: {num_like}, Comentario: {num_comentario}, Like Comentario: {num_likeComment} número hashtags: {indiceMail} \ntiempo que ha tardado programa: {total_tiempo_programa} \nfecha inicio: {fecha_inicio_formateada} fecha fin: {fecha_fin_formateada}'
                enviar_correo_correcto(bien_message)
            if max_retries == 2:
                indiceMail = indice + 1
                print(f"Seguir: {siguiendo}, Unfollow: {num_unfollow}, Like: {num_like}, Comentario: {num_comentario}, Like Comentario: {num_likeComment} número hashtags: {indiceMail} \ntiempo que ha tardado programa: {total_tiempo_programa} \nfecha inicio: {fecha_inicio_formateada} fecha fin: {fecha_fin_formateada}")
                bien_message = f'FB ENGLISH El programa ha realizado las siguientes operaciones \n\n Seguir: {siguiendo}, Unfollow: {num_unfollow}, Like: {num_like}, Comentario: {num_comentario}, Like Comentario: {num_likeComment} número hashtags: {indiceMail} \ntiempo que ha tardado programa: {total_tiempo_programa} \nfecha inicio: {fecha_inicio_formateada} fecha fin: {fecha_fin_formateada}'
                enviar_correo_correcto(bien_message)
            if max_retries == 1:
                indiceMail = indice + 1
                print(f"Seguir: {siguiendo}, Unfollow: {num_unfollow}, Like: {num_like}, Comentario: {num_comentario}, Like Comentario: {num_likeComment} número hashtags: {indiceMail} \ntiempo que ha tardado programa: {total_tiempo_programa} \nfecha inicio: {fecha_inicio_formateada} fecha fin: {fecha_fin_formateada}")
                bien_message = f'FB ENGLISH El programa ha realizado las siguientes operaciones \n\n Seguir: {siguiendo}, Unfollow: {num_unfollow}, Like: {num_like}, Comentario: {num_comentario}, Like Comentario: {num_likeComment} número hashtags: {indiceMail} \ntiempo que ha tardado programa: {total_tiempo_programa} \nfecha inicio: {fecha_inicio_formateada} fecha fin: {fecha_fin_formateada}'
                enviar_correo_correcto(bien_message)


            # Decrementar el número de intentos
            max_retries -= 1
            print(f"MAX RETRIES->  {max_retries}")
            with open(indice_filename, "w") as file:
                nexthashtag = 0               
                file.write(str(nexthashtag))
                print(f"--CONTINUANDO HASTAG despUes driver quit--------------{nexthashtag}")
            with open(indice_filename_tema, "w") as file:               
                file.write(str(max_retries))
                print(f"MAX RETRIES escritas->  {max_retries}")
                print(f"--tema hashtags:{TemaHastags} num hashtags totales: {numHashtag}")
                bien_message = f'-- FB ENGLISH HE TERMINADO = tema hashtags:{TemaHastags} num hashtags totales: {numHashtag}'
                enviar_correo_correcto(bien_message)
            print(f"+++ NUEVO LISTA HASHTAG +++")



            # Si se supera el número máximo de intentos, salir del bucle
        if max_retries == 0:
            with open(indice_filename_tema, "w") as file:
                max_retries = 3             
                file.write(str(max_retries))
                print(f"--write NEXT HASHTAG--------------{max_retries}")
            bien_message = f'FINALIZACION DEL PROGRAMA'
            enviar_correo_correcto(bien_message)
            print("--------------------------FINALIZACION DEL PROGRAMA--------------------------")
            break

    # Continuar con el resto del programa después de inicializar el WebDriver

if __name__ == "__main__":
    scriptFB2()

