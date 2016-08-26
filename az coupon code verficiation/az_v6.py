from selenium import webdriver
import time, sys, logging, argparse, time, random
from ConfigParser import SafeConfigParser
from apscheduler.schedulers.blocking import BlockingScheduler
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()

class AZCoupons:
    """ main class"""
    def __init__(self):
        self.verbosity = 'Y'

    def getElement(self, element, method):
        """Function to take xpath and return the element according to the method described
            element - elemt xpath, css, class name
            method - respective method - id, css, class name, xpath
            """        
        try:
            if method == 'class':
                return self.driver.find_element_by_class_name(element)
            elif method == 'css':
                return self.driver.find_element_by_css_selector(element)
            elif method == 'xpath':
                return self.driver.find_element_by_xpath(element)
            elif method == 'id':
                return self.driver.find_element_by_id(element)
        except:
            return None

    def returnText(self, elem):
        """Function to return the text value of the element
        elem - the element on the website
        """
        try:
            if str(((elem.text)).strip().replace(')','').replace('(','')):
                return str(((elem.text)).strip().replace(')','').replace('(',''))
            else:
                return None
        except:
            return None

    def verifyCoupon(self, asin, coupon, discount):
        """Function to verify whether a coupon is valid or not
        asin - asin of the product
        coupon - coupon code to be tested
        discount - discount that should be given
        """
        
        self.url = self.generateURL(asin)
        self.driver = webdriver.Firefox()
        self.driver.get(self.url)
        
        try:
            redirect = self.getElement('redir-opt-out-label', 'id')            
            redirect.click()
            self.getElement('redir-a-button-sec-center', 'class').click()
        except Exception,e:
            pass
            
        addToCart = self.getElement('add-to-cart-button', 'id')
        
        if addToCart !=None:
            addToCart.click()
            time.sleep(random.randint(1,3))            
           
            self.getElement('hlb-ptc-btn-native', 'id').click()
            time.sleep(random.randint(1,3))   
            
            self.getElement('ap_email', 'id').send_keys(self.email)
            time.sleep(random.randint(1,3))   
            self.getElement('ap_password', 'id').send_keys(self.pwd)
            time.sleep(random.randint(1,3))   
            self.getElement('signInSubmit', 'id').click()
            time.sleep(random.randint(1,3))   

            self.getElement('.a-declarative.a-button-text', 'css').click()
            time.sleep(random.randint(1,3))   
            self.getElement('a-button-text', 'class').click()
            time.sleep(random.randint(1,3))   
            self.getElement('gc-link-expander', 'id').click()
            time.sleep(random.randint(1,3))   
            self.getElement('gcpromoinput', 'id').send_keys(coupon)
            time.sleep(random.randint(1,3))   
            self.getElement('button-add-gcpromo', 'id').click()
            time.sleep(random.randint(1,3))   

            try:
                promo_ouput_elem = getElement('balance-checkbox', 'class')
                promo_text = returnText(promo_ouput_elem)                

                return 'Y', promo_text
            except:
                elem = self.getElement('gcpromoerrorblock', 'id')
                time.sleep(2)
                error = self.returnText(elem)
                print error
                return 'N', error
        else:
            return 'Product is not available for purchase on Amazon'
        self.driver.close()

    def getCoupons(self):
        pass

    def connectDB(self):
        pass

    def generateURL(self, asin):
        return 'http://www.amazon.com/gp/product/' + asin

    def parseConfig(self, configFile):
        """ Function to parse the config file
        configFile - name of the file
        """
        
        ## initializing the config parser
        parser = SafeConfigParser()
        parser.read(configFile)

        """ ## setting up static variables ## """              

        ## posting schedule
        self.year, self.month, self.day, week, day_of_week, hour, minute, second, useScheduler = parser.get('scheduler', 'year'), \
                                                                    parser.get('scheduler', 'month'), \
                                                                    parser.get('scheduler', 'day'), \
                                                                    parser.get('scheduler', 'week'),\
                                                                    parser.get('scheduler', 'day_of_week'), \
                                                                    parser.get('scheduler', 'hour'), \
                                                                    parser.get('scheduler', 'minute'), \
                                                                    parser.get('scheduler', 'second'),\
                                                                    parser.get('scheduler', 'useScheduler')

        ## amazon
        self.email, self.pwd = parser.get('amazon', 'email').replace("'",''), \
                              parser.get('amazon', 'pwd').replace("'",'')
        
        ## general settings
        self.verbosity = int(parser.get('settings', 'verbosity').replace("'",''))        

    def parseCMDArgs(self, arparser):
        """  Function to  parse the arguments from command line and overwrite default arguments
        arparser -- instance of the argparser
        """
        
        arparser.add_argument("-yr", "--year", help="year in which the scheduler should run. 4-digit year number")
        arparser.add_argument("-mm", "--month", help="month in which the scheduler should run. month number (1-12)")
        arparser.add_argument("-dd", "--day", help="day of month in which the scheduler should run. day of the month (1-31)")
        arparser.add_argument("-ww", "--week", help="week of year in which the scheduler should run. ISO week number (1-53)")
        arparser.add_argument("-hh", "--hour", help="hour of day in which the scheduler should run. hour (0-23)")
        arparser.add_argument("-mn", "--minute", help="minute of the hour in which the scheduler should run. minute (0-59)")
        arparser.add_argument("-ss", "--second", help="second in which the scheduler should run. second (0-59)")
        arparser.add_argument("-dw", "--day_of_week", help="day of week in which the scheduler should run. number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)")
        arparser.add_argument("-email", "--email", help="email of amazon account")
        arparser.add_argument("-pwd", "--pwd", help="password of amazon account")        
        arparser.add_argument("-v", "--verbosity", help="verbosity")
        arparser.add_argument('-t','--trigger', nargs='*', help="whether to trigger the argparser")
        arparser.add_argument("-a", "--asin", help="asin of the product")
        arparser.add_argument('-c','--coupon', nargs='*', help="coupon code to be tested")
        arparser.add_argument('-d','--discount', nargs='*', help="discount that should be visible")
        arparser.add_argument('-use','--useScheduler', nargs='*', help="whether to use scheduler")
            
        args = arparser.parse_args()

        return args

    def overWriteDefaultArgs(self, args):
        """ Function to overwrite the variables """
        if args.email:
            self.email = args.email
        if args.pwd:
            self.pwd = args.pwd    
        if args.verbosity:
            self.verbosity = int(args.verbosity)
        if self.verbosity:
            print 'Overwriting arguments from command line'   


configFile = 'config.cfg'
az = AZCoupons()
args = az.parseConfig(configFile)

arparser = argparse.ArgumentParser()
args = az.parseCMDArgs(arparser)

def main(asin, coupon, discount):       
    if args.trigger is not None:
        if args.asin and args.coupon and args.discount:
            asin = args.asin       
            coupon = args.coupon        
            discount = args.discount 
            az.overWriteDefaultArgs(args)

            if args.year:
                year = args.year
            if args.month:
                month = args.month
            if args.day:
                day = args.day
            if args.week:
                week = args.week
            if args.hour:
                hour = args.hour
            if args.minute:
                minute = args.minute
            if args.second:
                second = args.second
            if args.day_of_week:
                day_of_week = args.day_of_week
            if args.useScheduler:
                useScheduler = args.useScheduler
            else:
                useScheduler = 'N'

            if useScheduler == 'Y':        
                ## initialize the scheduler option. this is based on the local machine time
                ## runs at midnight 01-44-40
                sched.configure({'misfire_grace_time': 1000})
                @sched.scheduled_job('cron', year= year, month= month, day=day, week=week, \
                                     day_of_week=day_of_week, hour=hour, minute=minute, second=second)
                def timed_job():
                    logging.basicConfig()
                    print 'starting the job'
                    status, text = az.verifyCoupon(asin, coupon, discount)
                    
                sched.start()
            else:
                status, text = az.verifyCoupon(asin, coupon, discount)
        else:
            print 'ASIN, Coupon, and Discount required'
    else:
        status, text = az.verifyCoupon(asin, coupon, discount)

    return status
    sys.exit(1)

print main('B012X7ML36','EBJQ-GQ5UHX-Q4NL83', 6)
