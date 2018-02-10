# -*- coding: utf-8 -*-

import __builtin__
import pickle
import sys

import koding
import xbmcaddon
import xbmcplugin
from ..plugin import Plugin
from resources.lib.util.url import get_addon_url
from language import get_string as _


__builtin__.BOB_BASE_DOMAIN = "178.32.217.111"
ADDON = xbmcaddon.Addon()


class BoB(Plugin):
    name = "BoB"

    def first_run_wizard(self):
        import xbmcgui
        addon = xbmcaddon.Addon()
        dialog = xbmcgui.Dialog()
        addon_name = xbmcaddon.Addon().getAddonInfo('name')
        addon.setSetting("first_run", "false")
        if not dialog.yesno(addon_name, _("Run Setup Wizard?")):
            return
        if dialog.yesno(
                addon_name,
                "choose movie metadata provider",
                nolabel=_("TMDB"),
                yeslabel=_("TRAKT")):
            addon.setSetting("movie_metadata_provider", "Trakt")
        else:
            addon.setSetting("movie_metadata_provider", "TMDB")

        if dialog.yesno(
                addon_name,
                _("choose tv metadata provider"),
                nolabel=_("TVDB"),
                yeslabel=_("TRAKT")):
            addon.setSetting("tv_metadata_provider", "Trakt")
        else:
            addon.setSetting("tv_metadata_provider", "TVDB")

        if dialog.yesno(
                addon_name,
                _("choose Selector type"),
                nolabel=_("HD/SD"),
                yeslabel=_("Link Selector")):
            addon.setSetting("use_link_dialog", "true")
        else:
            default_links = [_("BOTH"), _("HD"), _("SD")]
            selected = dialog.select(_("choose default link"), default_links)
            if selected != -1:
                addon.setSetting("default_link", default_links[selected])

        themes = [
            "DEFAULT", "CARS", "COLOURFUL", "KIDS", "MOVIES", "SPACE",
            "GIF LIFE", "GIF NATURE", "USER"
        ]
        selected = dialog.select(_("choose theme"), themes)
        if selected != -1:
            addon.setSetting("theme", themes[selected])

        if dialog.yesno(addon_name, _("Enable GIF support?\n"),
                        _("May cause issues on lower end devices")):
            addon.setSetting("enable_gifs", "true")
        else:
            addon.setSetting("enable_gifs", "false")

        return True

    def get_theme_list(self):
        base_url = "http://www.norestrictions.club/norestrictions.club"
        base_theme_url = base_url + "/reloaded/themes/"
        theme_list = {
            'cars': [
                base_theme_url + "cars/cars1.jpg",
                base_theme_url + "cars/cars2.jpg",
                base_theme_url + "cars/cars3.jpg",
                base_theme_url + "cars/cars4.jpg",
                base_theme_url + "cars/cars5.jpg",
                base_theme_url + "cars/cars6.jpg",
                base_theme_url + "cars/cars7.jpg",
                base_theme_url + "cars/cars8.jpg",
                base_theme_url + "cars/cars9.jpg",
                base_theme_url + "cars/cars10.jpg",
            ],
            'colourful': [
                base_theme_url + "colourful/colourful1.jpg",
                base_theme_url + "colourful/colourful2.jpg",
                base_theme_url + "colourful/colourful3.jpg",
                base_theme_url + "colourful/colourful4.jpg",
                base_theme_url + "colourful/colourful5.jpg",
                base_theme_url + "colourful/colourful6.jpg",
                base_theme_url + "colourful/colourful7.jpg",
                base_theme_url + "colourful/colourful8.jpg",
            ],
            'kids': [
                base_theme_url + "kids/kids1.jpg",
                base_theme_url + "kids/kids2.jpg",
                base_theme_url + "kids/kids3.jpg",
                base_theme_url + "kids/kids4.jpg",
                base_theme_url + "kids/kids5.jpg",
                base_theme_url + "kids/kids6.jpg",
            ],
            'movies': [
                base_theme_url + "movies/movies1.jpg",
                base_theme_url + "movies/movies2.jpg",
                base_theme_url + "movies/movies3.jpg",
                base_theme_url + "movies/movies4.jpg",
                base_theme_url + "movies/movies5.jpg",
                base_theme_url + "movies/movies6.jpg",
                base_theme_url + "movies/movies7.jpg",
                base_theme_url + "movies/movies8.jpg",
                base_theme_url + "movies/movies9.jpg",
                base_theme_url + "movies/movies10.jpg",
                base_theme_url + "movies/movies11.jpg",
                base_theme_url + "movies/movies12.jpg",
            ],
            'space': [
                base_theme_url + "space/space1.jpg",
                base_theme_url + "space/space2.jpg",
                base_theme_url + "space/space3.jpg",
                base_theme_url + "space/space4.jpg",
                base_theme_url + "space/space5.jpg",
                base_theme_url + "space/space6.jpg",
                base_theme_url + "space/space7.jpg",
            ],
            'gif life': [
                base_theme_url + "giflife/city.gif",
                base_theme_url + "giflife/evUPmG6%20-%20Imgur.gif",
                base_theme_url + "giflife/night%20lights.gif",
                base_theme_url + "giflife/spinning%20wool.gif",
            ],
            'gif nature': [
                base_theme_url + "gifnature/falls.gif",
                base_theme_url + "gifnature/iceland.gif",
                base_theme_url + "gifnature/korea%20garden.gif",
                base_theme_url + "gifnature/sky%20waves.gif",
            ],
        }
        return theme_list

    def display_list(self, items, content_type):
        if content_type == "seasons":
            context_items = []
            if ADDON.getSetting("settings_context") == "true":
                context_items.append((_("Settings"),
                                     "RunPlugin({0})".format(
                                         get_addon_url("Settings"))))
            url = []
            for item in items:
                url.append(item["url"])
            koding.Add_Dir(
                name=_("All Episodes"),
                url=pickle.dumps(url),
                mode="all_episodes",
                folder=True,
                icon=ADDON.getAddonInfo("icon"),
                fanart=ADDON.getAddonInfo("fanart"),
                context_items=context_items,
                content_type="video")

        for item in items:
            context_items = []
            if ADDON.getSetting("settings_context") == "true":
                context_items.append((_("Settings"),
                                     "RunPlugin({0})".format(
                                         get_addon_url("Settings"))))
            context_items.extend(item["context"])
            koding.Add_Dir(
                name=item["label"],
                url=item["url"],
                mode=item["mode"],
                folder=item["folder"],
                icon=item["icon"],
                fanart=item["fanart"],
                context_items=context_items,
                content_type="video",
                info_labels=item["info"],
                set_property=item["properties"],
                set_art={"poster": item["icon"]})
        xbmcplugin.setContent(int(sys.argv[1]), content_type)
        return True

    def replace_url(self, url):
        if 'norestrictions.noobsandnerds.com' in url and 'norestrictions.club/norestrictions.club' not in url:
            url = url.replace('norestrictions.noobsandnerds.com',
                              __builtin__.BOB_BASE_DOMAIN)
        elif 'www.norestrictions.club' in url and 'www.norestrictions.club/norestrictions.club' not in url and 'norestrictions.club/norestrictions.club' not in url:
            url = url.replace('www.norestrictions.club',
                              __builtin__.BOB_BASE_DOMAIN)
        elif 'www.norestrictions.club/norestrictions.club' in url:
            url = url.replace(
                'www.norestrictions.club/norestrictions.club', __builtin__.BOB_BASE_DOMAIN)
        elif 'norestrictions.club' in url and 'norestrictions.club/norestrictions.club' not in url:
            url = url.replace('norestrictions.club', __builtin__.BOB_BASE_DOMAIN)
        elif 'norestrictions.club/norestrictions.club' in url:
            url = url.replace(
                'norestrictions.club/norestrictions.club', __builtin__.BOB_BASE_DOMAIN)
        return url

    def get_link_message(self, *args):
        messages = [
            {
                'HD': ' Zangetsu It\'s meaningless to just live, it\'s meaningless to just fight. I want to win',
                'SD': 'From this point on, all your opinions are rejected'
            },
            {
                'HD': 'Tensa Zangetsu',
                'SD': 'Sit upon the frosted heavens, Hyōrinmaru'
            },
            {
                'HD': 'Bankai',
                'SD': 'Sitting In Cinema Recording'
            },
            {
                'HD': 'Flower Wind Rage and Flower God Roar, Heavenly Wind Rage and Heavenly Demon Sneer!',
                'SD': 'This quality is sold on the corner by a shady guy'
            },
            {
                'HD': 'Reap your Enemy to Death, Kazeshini',
                'SD': 'Waiting For Dialup Connection'
            },
            {
                'HD': 'Getsuga Tensho ))))',
                'SD': 'Good Enough. I just want to watch'
            },
            {
                'HD': 'Sie hat nicht alle Tassen im Schrank',
                'SD': 'VHS Quality'
            },
            {
                'HD': 'Tsingtao ',
                'SD': 'Budweiser'
            },
            {
                'HD': 'Mensch meier und dickie eier',
                'SD': 'Flick probably sucks so lets just get it over'
            },
            {
                'HD': 'Looks like a Maserati',
                'SD': ' Looks like a Ford Focus'
            },
            {
                'HD': 'Supermodel Quality',
                'SD': ' Looks like Grandma Thelma'
            },
            {
                'HD': 'ARB',
                'SD': 'ARD'
            },
            {
                'HD': 'Merc the pinnacle of brilliance',
                'SD': 'The john harrison of quality'
            },
        ]

        if xbmcaddon.Addon().getSetting('enable_offensive') == 'true':
            messages.extend([
                {'HD': 'Kicks Ass!!',
                 'SD': 'Gets ass kicked repeatedly'
                 },
                {'HD': 'Howl, Zabimaru!!!',
                 'SD': 'Fucking Sucks!!'
                 },
                {'HD': 'Big Bodacious Breasts',
                 'SD': 'Saggy Milk Teats',
                 },
            ])
        return messages

    def get_searching_message(self, preset):
        messages = [
            '',
            'Bob\'s just nipping to blockbusters won\'t be but a sec',
            'Burn all creation to ash, Ryujinjakka!',
            'Bob\'s movie collection has no limits',
            'Searching the Internet for your selection',
            'Bob has seen your taste in movies and is very disappointed ',
            'Mein Englisch ist unter aller Sau',
            'Bob says you\'re a movie geek just like him',
            'Bob says get off of twitter and enjoy his addon',
            'Bob is a wanted man in 125 countries',
            'Bob said your taste in films is top notch',
            'When Bob chooses a movie, servers shake in fear',
            'They fear Bob. Don\'t listen to haters',
            'Bob said he works so hard for YOU, the end user',
            'Bob does this cause he loves it, not for greed',
            'That\'s not Bobs butt crack, it\'s his remote holder',
            'Bob...I Am Your Father!!',
            'I\'m going to make Bob an offer he can\'t refuse.',
            'Here\'s looking at you, Bob',
            'Go ahead, make Bob\'s day.',
            'May the Bob be with you',
            'You talking to Bob??',
            'I love the smell of Bob in the morning',
            'Bob, phone home',
            'Made it Bob! Top of the World!',
            'Bob, James Bob',
            'There\'s no place like Bob',
            'You had me at "Bob"',
            "YOU CAN\'T HANDLE THE BOB",
            'Round up all the usual Bobs',
            'I\'ll have what Bob\'s having',
            'You\'re gonna need a bigger Bob',
            'Bob\'ll be back',
            'If you build it. Bob will come',
            'We\'ll always have Bob',
            'Bob, we have a problem',
            'Say "hello" to my little Bob',
            'Bob, you\'re trying to seduce me. Aren\'t you?',
            'Elementary, my dear Bob',
            'Get your stinking paws off me, you damned dirty Bob',
            'Here\'s Bob!',
            'Hasta la vista, Bob.',
            'Soylent Green is Bob!',
            'Open the pod bay doors, BOB.',
            'Yo, Bob!',
            'Oh, no, it wasn\'t the airplanes. It was Beauty killed the Bob.',
            'A Bob. Shaken, not stirred.',
            'Who\'s on Bob.',
            'I feel the need - the need for Bob!',
            'Nobody puts Bob in a corner.',
            'I\'ll get you, my pretty, and your little Bob, too!',
            'I\'m Bob of the world!',
            'Shan of Bob',
            'Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb, Bøb',
            'We can rebuild Bob, we have the technology',
        ]

        if xbmcaddon.Addon().getSetting('enable_offensive') == "true":
            messages.extend([
                'Fuck Shit Wank -- Costa',
                'Frankly my dear, I don\'t give a Jen',
                'Beast Build Detected, Installing dangerous pyo file',
                'Costa wants to aduse Emma'
            ])

        if preset == "search":
            messages.extend([
                'Jen is popping in Blu Ray Disc'
            ])
        elif preset == "searchsd":
            messages.extend([
                'Jen rummaging through his vhs collection',
            ])

        return messages
