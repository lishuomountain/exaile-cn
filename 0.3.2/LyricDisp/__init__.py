# coding=utf-8

from xl import event, settings
import LyricDispprefs
import disp.Panel as Panel
import disp.Win as Win

PLAYERMODE = None
EXAILE =None

def ChangeMode(type, player, value):
    global PLAYERMODE, EXAILE
    options = {'LyricColor': settings.get_option('plugin/LyricDisp/lc' , '#43AAD0'), \
                'Opacity': float(settings.get_option('plugin/LyricDisp/op', '0.8')), \
                'LyricFolder': settings.get_option('plugin/LyricDisp/lf', '~/lyrics'), \
                'WindowPositionx': settings.get_option('plugin/LyricDisp/windowpositionx', 'centre'), \
                'WindowPositiony': settings.get_option('plugin/LyricDisp/windowpositiony', 'centre'), \
                'LyricSpacing': settings.get_option('plugin/LyricDisp/lyricspacing', '2'), \
                'Filename': settings.get_option('plugin/LyricDisp/ln' , 'artist-title.lrc')}
    settings.set_option('plugin/LyricDisp/ms',value)
    if PLAYERMODE <> value:
        if PLAYERMODE == '面板模式':
            Panel.disable(EXAILE)
            Win.enable(EXAILE, options)
        elif PLAYERMODE == '窗口模式':
            Win.disable(EXAILE)
            Panel.enable(EXAILE, options)
        PLAYERMODE = value

def enable(exaile):
    if (exaile.loading):
        event.add_callback(_enable, 'exaile_loaded')
    else:
        _enable(None, exaile, None)

def disable(exaile):
    if PLAYERMODE == '面板模式':
        Panel.disable(exaile)
    elif PLAYERMODE == '窗口模式':
        Win.disable(exaile)

def _enable(eventname, exaile, nothing):
    global PLAYERMODE, EXAILE
    options = {'LyricColor': settings.get_option('plugin/LyricDisp/lc' , '#43AAD0'), \
                'Opacity': float(settings.get_option('plugin/LyricDisp/op', '0.8')), \
                'LyricFolder': settings.get_option('plugin/LyricDisp/lf', '~/lyrics'), \
                'WindowPositionx': settings.get_option('plugin/LyricDisp/windowpositionx', 'centre'), \
                'WindowPositiony': settings.get_option('plugin/LyricDisp/windowpositiony', 'centre'), \
                'LyricSpacing': settings.get_option('plugin/LyricDisp/lyricspacing', '2'), \
                'Filename': settings.get_option('plugin/LyricDisp/ln' , 'artist-title.lrc')}
    PLAYERMODE = settings.get_option('plugin/LyricDisp/ms', '窗口模式')
    if PLAYERMODE == '面板模式':
        Panel.enable(exaile, options)
    elif PLAYERMODE == '窗口模式':
        Win.enable(exaile, options)
    event.add_callback(ChangeMode, 'mode_change')
    EXAILE = exaile
def get_preferences_pane():
    return LyricDispprefs
