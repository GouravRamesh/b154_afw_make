import pytest
from playwright.sync_api import sync_playwright
from pyjavaproperties import Properties
import os
import allure
class BaseTest:

    @pytest.fixture(autouse=True)
    def pre_condition(self,request):
        print("\n pre - condition")

        self.test_name=request.node.name
        print("started executing the test:",self.test_name)

        generics_path=os.path.dirname(__file__)
        self.framework_path=generics_path+"/.."

        self.xl_path=self.framework_path+"/data/input.xlsx"

        self.video_path = self.framework_path + "/videos/"
        print("video_path", self.video_path)

        config_path=self.framework_path+"/config.properties"
        print("read property file:",config_path)
        p=Properties()
        p.load(open(config_path))
        run_local=p['RUN_LOCAL']
        self.video=p["VIDEO"]
        remote_url=p["REMOTE_URL"]
        browser=p['BROWSER']
        app_url=p['APP_URL']
        nto=p['NTO']
        ato=p['ATO']

        print("start the playwright")
        self.playwright=sync_playwright().start()

        if run_local.lower()=="yes":
            print("Executing the script on local system")
            if browser=="chromium":
                print("open the chromium browser")
                self.browser=self.playwright.chromium.launch(headless=True)
            elif browser=="firefox":
                print("open the firefox browser")
                self.browser=self.playwright.firefox.launch(headless=True)
            else:
                print("open the webkit(safari) browser")
                self.browser = self.playwright.webkit.launch(headless=True)

        else:
            print("Executing the script on remote system")
            if browser == "chromium":
                print("open the chromium browser")
                self.browser = self.playwright.chromium.connect(remote_url)
            elif browser == "firefox":
                print("open the firefox browser")
                self.browser = self.playwright.firefox.connect(remote_url)
            else:
                print("open the webkit(safari) browser")
                self.browser = self.playwright.webkit.connect(remote_url)

        if self.video.lower() == "yes":
            self.context = self.browser.new_context(
                record_video_dir=self.video_path,
                viewport={"width": 1280, "height": 720},
                record_video_size={"width": 1280, "height": 720})
        else:
            self.context = self.browser.new_context()

        print("go to the new page")
        self.page=self.context.new_page()

        print("set naviation timeout to:",nto,'ms')
        self.page.set_default_navigation_timeout(float(nto))

        print("set default timeout to",ato,'ms')
        self.page.set_default_timeout(float(ato))

        print("enter the url:",app_url)
        self.page.goto(app_url)


    @pytest.fixture(autouse=True)
    def post_condition(self,request):
        yield
        print("\npost condition")

        if request.node.call.failed:
            print("Test is Failed and Taking screenshot")
            allure.attach(self.page.screenshot(),name=self.test_name,
                              attachment_type=allure.attachment_type.PNG)
        else:
            print("Test is Passed and NOT Taking screenshot")

        print("close the page")
        self.page.close()

        if self.video.lower() == "yes":
            print(f"saving video:{self.test_name}.webm")
            video_file = f"{self.video_path}{self.test_name}.webm"
            self.page.video.save_as(video_file)
            self.page.video.delete()

            print("attaching video to allure")
            allure.attach.file(video_file,name=self.test_name,
                               attachment_type=allure.attachment_type.WEBM,
                               extension="webm")

        print("close the context")
        self.context.close()

        print("close the browser")
        self.browser.close()

        print("stop the playwright")
        self.playwright.stop()
