from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from datetime import datetime
from time import time
import time

def main():

  #WEBDRIVER CONFIG
  driver_path = "edgedriver_win64/msedgedriver.exe"
  service = Service(driver_path)
  options = Options()
  options.use_chromium = True
  options.add_argument("--log-level=3")
  # options.add_argument("--window-size=600,600")
  driver = webdriver.Edge(options, service)
  #INPUT
  search_term = input("Enter a search term to find products:\n")

  Path("results").mkdir(parents=True, exist_ok=True)

  #FILE HEADINGS
  filename = search_term+"_"+str(time.time()*1000)
  stream = open("results/"+filename+".txt", "a")
  stream.write(f"Seacrh term: '{search_term}'\n")
  stream.write(f"DateTime: {datetime.now()}\n")
  stream.write("--------------------------------------------\n")
  stream.close()

  product_counter = 0
  page_counter = 0
  #LOOP THROUGH ALL PAGES 
  while True:
    page_counter += 1
    search_url = "https://www.homedepot.com.mx/s/"+search_term+"?pag="+str(page_counter)


    #LOAD PAGE
    try:
      driver.get(search_url)
      driver_wait = WebDriverWait(driver=driver,timeout=10.0)
      element = driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "app")))
      print(f"[{datetime.now()}]:Page loaded ({page_counter})")
      time.sleep(5.0)
    except Exception as e:
      print("Cannot open page:",page_counter,"\nEnd of program")

    #CLOSE POPUP
    try:
      webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
      print(f"[{datetime.now()}]:Closing Pop up")
      time.sleep(5.0)
    except Exception as e:
      print("Attempt to close pop up window fail.", e)

    #SCROLL DOWN SCRIPT
    try:
      driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
      print(f"[{datetime.now()}]:Scrolling to the bottom of the page")
    except Exception as e:
      print("Attempt to scroll down to bottom fail.",e)    

    #FETCH ELEMENTS
    try:
      common_container = driver.find_element(By.XPATH, "//*[@id=\"search\"]/div[6]/div[2]/div[4]/span/div/div[2]")
      product_containers = common_container.find_elements(By.CSS_SELECTOR,".product-card-padding")
      print(f"[{datetime.now()}]:Found {len(product_containers)} items.")

      if len(product_containers) == 0:
        raise IndexError
      for container in product_containers:
        product_counter += 1
        base_element = container.find_element(By.CSS_SELECTOR,".product-card .product-card-shadow .MuiGrid-root .MuiGrid-root .MuiCardContent-root .styled--productcard-container")

        brand= base_element.find_element(By.CSS_SELECTOR,".styled--productcard-basicinfo .styled--productcard-title .MuiTypography-root span.product-brand").text
        description= base_element.find_element(By.CSS_SELECTOR,".styled--productcard-basicinfo .styled--productcard-title .MuiTypography-root a").text
        link= "https://www.homedepot.com.mx"+base_element.find_element(By.CSS_SELECTOR,".styled--productcard-basicinfo .styled--productcard-title .MuiTypography-root a").get_dom_attribute("href")
        price= base_element.find_element(By.XPATH,"(./div)[4]/div[1]/div[1]/div[2]/p[1]").text
        #FORMAT PRICE
        price = price[:-3]+"."+price[-3:]
        #SAVE DATA
        stream = open("results/"+filename+".txt", "a")
        stream.write(f"({product_counter}):{brand} - {description} - {price} - {link}\n")
        stream.close()

    except Exception as e:
      print(f"[{datetime.now()}]:No elements found")   

      #CLOSE WEBDRIVER
      try:
        print(f"[{datetime.now()}]:Closing Webdriver")
        driver.quit()
      except Exception as e:
        print("Attempt to close web driver fail.",e)
      print(f"[{datetime.now()}]:End of program")
      exit()


if __name__ == "__main__":
  main()

  