from selenium.webdriver.common.by import By

class HandyWrappers:
    # Constructor to initialize the driver instance
    def __init__(self, driver):
        self.driver = driver

    # Method to get the appropriate Selenium locator type
    def getByType(self, LocatorType):
        LocatorType = LocatorType.lower()
        if LocatorType == 'id':
            return By.ID
        elif LocatorType == 'name':
            return By.NAME
        elif LocatorType == 'xpath':
            return By.XPATH
        elif LocatorType == 'classname':
            return By.CLASS_NAME
        elif LocatorType == 'css':
            return By.CSS_SELECTOR
        elif LocatorType == 'linktext':
            return By.LINK_TEXT
        elif LocatorType == 'tagname':
            return By.TAG_NAME
        else:
            # Print error message if an unsupported or incorrect locator type is passed
            print("Locator Type " + LocatorType + " not Correct or Supported")
        return False

    # Method to find and return a single element using the given locator and locator type
    def GetElement(self, Locator, LocatorType='id'):
        element = None
        try:
            LocatorType = LocatorType.lower()
            ByType = self.getByType(LocatorType)
            element = self.driver.find_element(ByType, Locator)
            return element
        except:
            # Return None if the element is not found or any error occurs
            return element

    # Method to find and return a list of elements matching the locator and locator type
    def GetElements(self, Locator, LocatorType='id'):
        Elements = []
        try:
            LocatorType = LocatorType.lower()
            ByType = self.getByType(LocatorType)
            Elements = self.driver.find_elements(ByType, Locator)
            if Elements not in [None, False]:
                print("Elements found")
            else:
                print("Elements list empty!")
        except:
            print("Elements Error!")
        return Elements

    # Method to click on an element if it's present
    def ClickElement(self, Locator, LocatorType='id'):
        try:
            Get_Element = self.GetElement(Locator, LocatorType)
            if Get_Element is not None or False:
                Get_Element.click()
                print('Element Clicked')
            else:
                pass
        except:
            pass

    # Method to extract and return the text from an element
    def GetElementText(self, Locator, LocatorType='id'):
        Element_text = ''
        try:
            Get_Element = self.GetElement(Locator, LocatorType)
            if Get_Element is not None or False:
                Element_text = Get_Element.text
            else:
                print("Element does not have any text")
        except:
            print('Element Error!')
        return Element_text

    # Method to extract text from multiple elements and return a list of their texts
    def GetElementlistofText(self, Locator, LocatorType='id'):
        list_of_Text = []
        try:
            ElementlistofText = self.GetElements(Locator, LocatorType)
            for elements in ElementlistofText:
                if elements not in [None, False]:
                    text_elements = elements.text
                    list_of_Text.append(text_elements)
                else:
                    print("Element list not exist!")
        except:
            print('Element error!')
        return list_of_Text

    # Method to retrieve the value of a specific attribute from an element
    def GetElementAttribute(self, Locator, LocatorType='id', attribute='class'):
        attribute_value = None
        try:
            Element = self.GetElement(Locator, LocatorType)
            if Element not in [None, False]:
                attribute_value = Element.get_attribute(attribute)
            else:
                print("Value of attribute does not exist")
        except:
            print('Value of attribute has error')
        return attribute_value

    # Method to get a list of attribute values for multiple elements
    def GetElementlistofattribute(self, Locator, LocatorType='id', attribute='class'):
        list_of_attribute = []
        try:
            elements = self.GetElements(Locator, LocatorType)
            for element in elements:
                if element not in [None, False]:
                    attribute_value = element.get_attribute(attribute)
                    list_of_attribute.append(attribute_value)
                else:
                    print('list of attribute value is empty')
        except:
            print('list of attribute value error')
        return list_of_attribute

    # Method to check if an element is present on the page
    def isElementPresent(self, Locator, LocatorType='id'):
        try:
            element = self.GetElement(Locator, LocatorType)
            if element is not None:
                return True
            else:
                return False
        except:
            return False
