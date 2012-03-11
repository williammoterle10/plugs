def _get_portrait_image_filename(id):
    import os
    return os.path.join('portraits', str(id) + '.tmp' + '.jpg')

def _get_portrait_image_thumbnail(id, size=50):
    import os
    return os.path.join('portraits', str(id) + '.%dx%d' % (size, size) + '.jpg')

def get_user_image(user, size=50):
    from uliweb import functions
    import os
    
    image = functions.get_filename(_get_portrait_image_thumbnail(user.id, size))
    if os.path.exists(image):
        image_url = functions.get_href(_get_portrait_image_thumbnail(user.id, size))
    else:
        image_url = user.get_default_image_url(size)
    return image_url
    
