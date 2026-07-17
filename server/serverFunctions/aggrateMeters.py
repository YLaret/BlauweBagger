def aggrateMeters(meters):
    # mix
    if meters[3]["Value"] == 1 and meters[4]["Value"] == 1:
        mix = "VOL"
    elif meters[3]["Value"] == 0 and meters[4]["Value"] == 1:
        mix = "OK"
    elif meters[3]["Value"] == 0 and meters[4]["Value"] == 0:
        mix = "LOW"
    else:
        mix = "ERROR"
        
    # vuil
    if meters[5]["Value"] == 1 and meters[6]["Value"] == 1:
        vuil = "VOL"
    elif meters[5]["Value"] == 0 and meters[6]["Value"] == 1:
        vuil = "OK"
    elif meters[5]["Value"] == 0 and meters[6]["Value"] == 0:
        vuil = "LOW"
    else:
        vuil = "ERROR"
    
    # schoon
    if meters[7]["Value"] == 1 and meters[8]["Value"] == 1:
        schoon = "VOL"
    elif meters[7]["Value"] == 0 and meters[8]["Value"] == 1:
        schoon = "OK"
    elif meters[7]["Value"] == 0 and meters[8]["Value"] == 0:
        schoon = "LOW"
    else:
        schoon = "ERROR"

    return {'mix':mix,'vuil':vuil,'schoon':schoon}
