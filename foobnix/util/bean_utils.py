#-*- coding: utf-8 -*-
'''
Created on 20 окт. 2010

@author: ivan
'''
import os
import logging
from foobnix.gui.model import FDModel, FModel

from foobnix.util.text_utils import normalize_text
from foobnix.fc.fc import FC
from foobnix.fc.fc_cache import FCache

def update_parent_for_beans(beans, parent):
    for bean in beans:
        if not bean.get_is_file():
            bean.parent(parent)


"""update bean info form text if possible"""
def update_bean_from_normalized_text(bean):

    if not bean.artist or not bean.title:
        bean.text = normalize_text(bean.text)

        text_artist = bean.get_artist_from_text()
        text_title = bean.get_title_from_text()

        if text_artist and text_title:
            bean.artist, bean.title = text_artist, text_title
    return bean


def get_bean_posible_paths(bean):
    logging.debug("get bean path: %s" % bean)
    path = get_bean_download_path(bean, path=FC().online_save_to_folder)
    if path and os.path.exists(path):
        return path

    for paths in FCache().music_paths:
        for path in paths:
            path = get_bean_download_path(bean, path)
            if path and os.path.exists(path):
                return path

    return None


def get_bean_download_path(bean, path=FC().online_save_to_folder, nosubfolder = FC().nosubfolder):

    ext = ".mp3"
    if nosubfolder:
        name = bean.get_display_name()
        name = name.replace("/", "-")
        name = name.replace("\\", "-")
        path = os.path.join(path, name + ext)
        return path
    elif bean.artist:
        bean.artist = bean.artist.replace("/", "-")
        bean.artist = bean.artist.replace("\\", "-")
        path = os.path.join(path, bean.artist, bean.get_display_name() + ext)
        logging.debug("bean path %s" % path)
        return path
    else:
        logging.debug("get bean path: %s" % bean)
        path = os.path.join(path, bean.get_display_name() + ext)
        logging.debug("bean path %s" % path)
        return path


def get_bean_from_file(f):
    if not os.path.exists(f):
        logging.debug("not exists" + str(f))
        return None
    bean = FDModel(text=os.path.basename(f), path=f)
    is_file = True if os.path.isfile(f) else False
    bean = bean.add_is_file(is_file)
    if not is_file:
        bean.add_font("bold")
    return bean
