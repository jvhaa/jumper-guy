textindex = "abcdefghijklmnopqrstuvwxyz0123456789 "

def text(game, surf, coords, text, variant = "normal"):
        width = 0
        for word in text:
            if variant == "normal":
                img = game.assets["alphabet"][textindex.index(word)]
            else:
                 img = game.assets["alphabet"][textindex.index(word)]
            surf.blit(img, (coords[0]+width, coords[1]))
            width += img.get_width()+2