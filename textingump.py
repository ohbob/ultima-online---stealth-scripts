import time

def textingump(text: str = "None", buttonid: int = None, timeout: int = 90) -> bool:
    """Search for text/xml in a gump, if found press buttonid
     Args:
        text (str): name to search for
        buttonid (int): button id to press if text found
        timeout (int): expiration of loop timeout
    Returns:
        bool: True / False
    """
    found: bool = False
    gumptimeout = time.time()

    while not found and gumptimeout + timeout > time.time():
        for i in range(GetGumpsCount()):
            gump = GetGumpInfo(i)
            gumpindex = i
            if len(gump['XmfHTMLGumpColor']):
                for x in gump['XmfHTMLGumpColor']:
                    if text.upper() in GetClilocByID(x['ClilocID']).upper():
                        found = True
                        break
            else:
                if len(gump['Text']):
                    for x in gump['Text']:
                        if text.upper() in x[0].upper():
                            found = True
                            break
        Wait(50)

    if found and buttonid is not None:
        NumGumpButton(gumpindex, buttonid)

    return found
