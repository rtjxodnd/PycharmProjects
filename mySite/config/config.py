# chromeDriverPath return
def chromeDriverPath(area="ubuntu"):
    if area == "test":
        chromeDriverPath = "chromedriver/chromedriver_windows.exe"
    elif area == "ubuntu":
        chromeDriverPath = "chromedriver/chromedriver_ubuntu"
    else:
        chromeDriverPath = "chromedriver/chromedriver_ubuntu"
        chromeDriverPath = ""
    return chromeDriverPath