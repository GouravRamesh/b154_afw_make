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
        self.page.goto(app_url, wait_until="domcontentloaded")


    @pytest.fixture(autouse=True)
    def post_condition(self,request):
        yield
        print("\npost condition")

        setup_report = getattr(request.node, 'setup', None)
        call_report = getattr(request.node, 'call', None)
        failed = (setup_report is not None and setup_report.failed) or \
                 (call_report is not None and call_report.failed)

        page = getattr(self, 'page', None)

        if failed and page is not None:
            print("Test is Failed and Taking screenshot")
            try:
                allure.attach(page.screenshot(),name=self.test_name,
                                  attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print("screenshot failed:", e)
        else:
            print("Test is Passed or no page — NOT Taking screenshot")

        if page is not None:
            try:
                print("close the page")
                page.close()
            except Exception as e:
                print("page close failed:", e)

            if self.video.lower() == "yes":
                try:
                    print(f"saving video:{self.test_name}.webm")
                    video_file = f"{self.video_path}{self.test_name}.webm"
                    page.video.save_as(video_file)
                    page.video.delete()
                    print("attaching video to allure")
                    allure.attach.file(video_file,name=self.test_name,
                                       attachment_type=allure.attachment_type.WEBM,
                                       extension="webm")
                except Exception as e:
                    print("video save failed:", e)

        context = getattr(self, 'context', None)
        if context is not None:
            try:
                print("close the context")
                context.close()
            except Exception as e:
                print("context close failed:", e)

        browser = getattr(self, 'browser', None)
        if browser is not None:
            try:
                print("close the browser")
                browser.close()
            except Exception as e:
                print("browser close failed:", e)

        playwright = getattr(self, 'playwright', None)
        if playwright is not None:
            try:
                print("stop the playwright")
                playwright.stop()
            except Exception as e:
                print("playwright stop failed:", e)
