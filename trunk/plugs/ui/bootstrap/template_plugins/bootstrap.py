def call(app, var, env, plugins=None, use_less=False):
    plugins = plugins or []
    a = []
    a.append('<!--[if lt IE 9]>')
    a.append('bootstrap/asset/html5.js')
    a.append('<![endif]-->')
    if use_less:
        a.append('bootstrap/lib/bootstrap.less')
    else:
        a.append('bootstrap/bootstrap.min.css')
    
    jquery = False
    for x in plugins:
        a.append('bootstrap/js/bootstrap-%s.js' % x)
        jquery = True
      
    d = {'toplinks':a, 'depends':[]}
    if jquery:
        d['depends'] = ['jquery']
    if use_less:
        d['depends_after'] = ['less']
        
    return d
