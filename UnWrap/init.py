from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from webdriver_manager.chrome import ChromeDriverManager

from SaverImage.init import ImagesSaver

tempFilms = None
tempSerials = None

class UnWap:
    def __init__(self, ip):
        self.ip = ip
        self.baseUrl = "https://ma.anwap.movie"
        self.imageSaver = ImagesSaver("UnWrap", ip)
        self.driverPath = Path(__file__).parent.parent.parent.parent / "chromedriver"
        # self.driverPath = r"/home/a0557915/domains/request.denishik.ru/limboServer/chromedriver"
        self.films = self.baseUrl + "/films"
        self.serials = self.baseUrl + "/serials"

        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        try:
            webdriver.Chrome(ChromeDriverManager().install(), chrome_options=self.options)
            print("✅ VRCatRoutes/UnWap")
        except Exception as e:
            print("X VRCatRoutes/UnWap> path: " + str(self.driverPath))
            print("X VRCatRoutes/UnWap> Error: " + str(e))

    def getData(self, results):
        tempList = []
        images = []
        for result in results:
            title = ""
            image = ""
            url = ""
            try:
                # title = WebDriverWait(result, 2).until(
                #     EC.presence_of_element_located((By.CLASS_NAME, "namefilm"))
                # )
                title = result.find_element(By.CLASS_NAME, "namefilm")
                title = title.text
                print(title)
            except Exception as e:
                print(">" + str(e))
            try:

                # image = WebDriverWait(result, 2).until(
                #     EC.presence_of_element_located((By.CLASS_NAME, "screenf"))
                # )
                image = result.find_element(By.CLASS_NAME, "screenf")
                image = image.get_attribute("src")
            except Exception as e:
                print(">" + str(e))
            images.append(image)
            try:
                # url = WebDriverWait(result, 2).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
                url = result.find_element(By.TAG_NAME, "a")
                url = url.get_attribute("href")
            except Exception as e:
                print(">" + str(e))
            driverD = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=self.options)
            driverD.get(url)
            downloads = driverD.find_elements(By.CLASS_NAME, "blms")
            listR = []
            if (len(downloads) > 0):
                downloads = downloads[len(downloads) - 1].find_elements(By.TAG_NAME, "a")
                for download in downloads:
                    if ("x" in download.text):
                        listR.append(download.get_attribute("href"))
                        print(download.text)

            if (len(listR) > 0):
                download = listR[len(listR) - 1]
                print(download)
            else:
                download = ""

            tempList.append({
                "name": title,
                "image": image,
                "download": download
            })

        self.imageSaver.saveImages(images)
        return tempList

    def getSearials(self, search = None):
        try:
            global tempSerials
            images = []
            if (search == None and tempSerials != None):
                for item in tempSerials:
                    images.append(item["image"])
                self.imageSaver.saveImages(images)
                return tempSerials

            chrome_options = Options()
            chrome_options.add_argument("user-data-dir=selenium")
            driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=self.options)
            if (search != None):
                print(self.serials + f"/search/?word={search}&vid=1")
                driver.get(self.serials + f"/search/?word={search}&vid=1")
            else:
                print(self.serials + "/top")
                driver.get(self.serials + "/top")

            try:
                error = driver.find_element(By.CLASS_NAME, "err")
                if (error.text == "К сожалению по вашему запросу в названии"):
                    return []
            except:
                pass

            results = driver.find_elements(By.CLASS_NAME, "film")
            data = self.getData(results)
            tempSerials = data
            return data

        except Exception as e:
            print(e)
            return None


    def getFilms(self, search = None):
        try:
            global tempFilms
            images = []
            if (search == None and tempFilms != None):
                for item in tempFilms:
                    images.append(item["image"])
                self.imageSaver.saveImages(images)
                return tempFilms

            chrome_options = Options()
            chrome_options.add_argument("user-data-dir=selenium")
            driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=self.options)
            if (search != None):
                print(self.films + f"/search/?word={search}&vid=1")
                driver.get(self.films + f"/search/?word={search}&vid=1")
            else:
                print(self.films + "/top")
                driver.get(self.films + "/top")

            try:
                error = driver.find_element(By.CLASS_NAME, "err")
                if (error.text == "К сожалению по вашему запросу в названии"):
                    return []
            except:
                pass

            results = driver.find_elements(By.CLASS_NAME, "film")
            data = self.getData(results)
            tempFilms = data
            return data

        except Exception as e:
            print(e)
            return None

