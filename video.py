# import streamlit as st
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# import time

# def open_and_click(tt):
#     chrome_options = Options()
#     chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
#     chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.media_stream": 1})

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
#     try:
#         driver.get(f"https://www.imdb.com/title/{tt}/")
        
#         # Esperar hasta que el elemento esté disponible
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "ipc-lockup-overlay.sc-c8d6e64c-0.dOyAfp.videoplayer__slate-reactions.ipc-focusable"))
#         )
#         try:
#             element = driver.find_element(By.CLASS_NAME, "ipc-lockup-overlay.sc-c8d6e64c-0.dOyAfp.videoplayer__slate-reactions.ipc-focusable")
#             href = element.get_attribute("href")
#             if href:
#                 driver.get(href)
#             else:
#                 st.warning("No se encontró el enlace. Mostrando la página inicial.")
#         except Exception as e:
#             st.warning(f"No se encontró el enlace para hacer clic: {e}. Mostrando la página inicial.")
        
#       #   element = driver.find_element(By.CLASS_NAME, "ipc-lockup-overlay.sc-c8d6e64c-0.dOyAfp.videoplayer__slate-reactions.ipc-focusable")
#       #   href = element.get_attribute("href")
#       #   driver.get(href)
#     except Exception as e:
#         print(f"Error al encontrar o hacer clic en el elemento: {e}")
#     finally:
#         time.sleep(20)  # Esperar un momento para ver el resultado
#         driver.quit()


import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def open_and_click(tt):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.media_stream": 1})

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(f"https://www.imdb.com/title/{tt}/")
        
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ipc-lockup-overlay"))
        )
        
        href = element.get_attribute("href")
        if href:
            driver.get(href)
            st.success("Video loaded successfully!")
        else:
            st.warning("No se encontró el enlace. Mostrando la página inicial.")
        
        time.sleep(5)
        
        return driver.current_url
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None
        
    finally:
        if 'driver' in locals():
            driver.quit()