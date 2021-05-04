from flask import Flask, request, redirect, url_for, send_from_directory
import glob
import markdown2
import mf2py
from os import path

app = Flask(__name__, static_url_path='')
currentresource = ""
cssstate = "day"
css = ""
htmlPrefix = ""
htmlPostfix = ""
hcardurl = "http://jamesstallings.code4peeps.life"
hcard = dict()

""" siteroot = "site/"
siteimages = "images/"
sitemarkdown = "markdown/" """

siteroot = "./site/"
siteimages = ""
sitemarkdown = ""

mdfile = ""

def sethtmlbasis():
    global sitemarkdown
    global htmlPrefix
    global htmlPostfix
    global hcard
    global hcardurl
    global css
    global cssstate
    global mdfile

    cssfile = "writer-%s.css" % cssstate

    print("CSS file selected: %s" % cssfile)

    if path.exists(cssfile):
        with open(cssfile) as f:
            css = f.read()
        print("CSS %s read" % cssfile)

    hcard = mf2py.parse(url=hcardurl)

    if 'items' in hcard:
        name = hcard['items'][0]['properties']['name']
        nickname = hcard['items'][0]['properties']['nickname']
        photourl = hcard['items'][0]['properties']['photo']
        org = hcard['items'][0]['properties']['org']
        title = hcard['items'][0]['properties']['job-title']
        role = hcard['items'][0]['properties']['role']
        email = hcard['items'][0]['properties']['email']
        phone = hcard['items'][0]['properties']['tel']
        note0 = hcard['items'][0]['properties']['note']
    else:
        name = 'N/A'
        nickname = 'N/A'
        photourl = 'nobody.png'
        org = 'none'
        title = 'empty'
        role = 'unassigned'
        email = 'mailto: nobody@mailinator.com'
        phone = '800 one song'
        note0 = 'this is a default h-card'

    htmlPrefix = """
 <!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width">

  <title>Write: Read-Write, the read-write web. The web for Humans</title>
  <script type="module">
    document.documentElement.classList.remove('no-js');
    document.documentElement.classList.add('js');
  </script>

  <meta name="description" content="Digital Presence of James Stallings">
  <meta property="og:title" content="code4peeps">
  <meta property="og:description" content="content rendering">
  <meta property="og:image" content="http://static.code4peeps.life/me.jpg">
  <meta property="og:image:alt" content="selfie">
  <meta property="og:locale" content="en_US">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://reader.code4peeps.life/reader/index.md">
  <link rel="canonical" href="http://reader.code4peeps.life/reader/index.md">
  <link rel="icon" href="/favicon.ico">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/my.webmanifest">
  <meta name="theme-color" content="#FF00FF">
</head> 
  <style type=text/css>""" + css + """</style>
  <body>
  <span id="h-card" class="h-card">
    <table>
      <tr>
        <td rowspan=4>
            <image style="width: 120px; height: 120px" src="%s" alt="James Stallings Photo">
        </td>
        <td><table>
          <tr>
            <td colspan=2>
                <h1>WRITER - the read-write web. The web for humans.
            </td>
          </tr>
          <tr>
            <td>
                Name: %s aka %s
            </td>
            <td>
                Org/Title: %s/%s, %s
            </td>
          </tr>
          <tr>
            <td>
                h-card url: %s
            </td>
            <td>
              e-mail: %s
            </td>
          </tr>
          <tr>
            <td>
              phone# %s
            </td>
            <td>
              %s
            </td>
          </tr></table>
        </td>
      </tr>
    </table>
  </span>""" % (photourl[0], name[0], nickname[0], org[0], title[0], role[0], hcardurl[0], email[0], phone[0], note0[0])

    htmlPostfix = """
    <footer>
      <h6>A complete <a href="https://www.markdownguide.org/basic-syntax/" target="top">markdown reference</a> is available</h6>
      <h6><a href="#open-modal">system menu</a></h6>
      <div id="open-modal" class="modal-window">
        <div>
          <a href="#modal-close" title="close" class="modal-close">close &times;</a>
          <h1>system menu</h1>
          <div><a href='http://localhost:7000/togglecss'>toggle CSS</a><div>
        </div>
      </div>
    </footer>
  </body>
</html>"""    

"""    file_name = siteroot + sitemarkdown + mdfile + ".pre"
    if mdfile != "" and path.exists(file_name):
        with open(file_name) as f:
            htmlPrefix = f.read()
        print(" * html prologue %s read" % file_name)

    file_name = siteroot + sitemarkdown + mdfile + ".post"
    if mdfile != "" and path.exists(file_name):
        with open(file_name) as f:
            htmlPostfix = f.read()
        print(" * html epilogue %s read" % file_name)
"""
def redirect_url():
    return request.args.get('next') or request.referrer or url_for('index')

@app.route('/togglecss', methods=['GET'])
def togglecss():
    global cssstate
    global css
    global htmlPrefix
    global htmlPostfix

    if cssstate == "night":
        cssstate = "day"
    else:
        cssstate = "night"

    sethtmlbasis()
    return redirect(redirect_url())

@app.route('/writemarkdown', methods=['POST'])
def writemarkdown():
    global htmlPrefix
    global htmlPostfix
    global mdfile

    mdfile = request.form['filename']

    if request.form['submit'] == 'cancel':
        return redirect('http://localhost:7000/writer/' + mdfile)
    elif request.form['submit'] == 'done':

        file_name = siteroot + sitemarkdown + mdfile
        print("Writing file %s" % file_name)
        with open(file_name, 'w') as f:
            f.write(request.form['markdowntxt'])
        print("File %s written" % file_name) 

        sethtmlbasis()

        file_name = siteroot + sitemarkdown + mdfile + ".pre"
        print("Writing file %s" % file_name)
        with open(file_name, 'w') as f:
            f.write(htmlPrefix)
        print("File %s written" % file_name) 

        file_name = siteroot + sitemarkdown + mdfile + ".post"
        print("Writing file %s" % file_name)
        with open(file_name, 'w') as f:
            f.write(htmlPostfix)
        print("File %s written" % file_name) 

        return redirect('http://localhost:7000/writer/' + request.form['filename'])
        

@app.route('/createnewmarkdown/<filename>', methods=['GET'])
def createnewmarkdown(filename):
    global htmlPrefix
    global htmlPostfix
    global mdfile

    mdfile = mdfile

    return htmlPrefix + """
<form method='POST' action="/writemarkdown" role='form'>
<textarea id='markdowntxt' name='markdowntxt' rows='32' cols='120'>
""" + "be somebody" + """
</textarea>
<br>
<input type="hidden" name="filename" value=""" + filename + """>
<input type='submit' name='submit' value='done'>
<input type='submit' name='submit' value='cancel'>
</form>
""" + htmlPostfix


@app.route('/editmarkdown/<filename>', methods=['GET'])
def editmarkdown(filename):
    global htmlPrefix
    global htmlPostfix
    global mdfile

    file_name = siteroot + sitemarkdown + filename
    if path.exists(file_name):
        mdfile = filename
        with open(file_name) as f:
            read_data = f.read()
            f.close()

        return htmlPrefix + """
<form method='POST' action="/writemarkdown" role='form'>
<textarea id='markdowntxt' name='markdowntxt' rows='32' cols='120'>
""" + read_data + """
</textarea>
<br>
<input type="hidden" name="filename" value=""" + filename + """>
<input type='submit' name='submit' value='done'>
<input type='submit' name='submit' value='cancel'>
</form>
""" + htmlPostfix
    else:
        return htmlPrefix + markdown2.markdown('*404* NOTFOUND\n\r',extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + htmlPostfix


@app.route('/writer/')
def renderdefaultview():
    global htmlPrefix
    global htmlPostfix
    global siteroot
    global sitemarkdown
    global mdfile

    if path.exists(siteroot + sitemarkdown + 'index.md'):
        mdfile = "index.md"
        with open(siteroot + sitemarkdown + 'index.md') as f:
            read_data = f.read()

        return htmlPrefix + "<br><h6><a href='http://localhost:7000/editmarkdown/index.md'>edit index.md</a></h6><br>" + markdown2.markdown(read_data, extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + htmlPostfix
    else:
        scripts = ""
        for file_name in glob.iglob('./*.md', recursive=True):
            scripts = scripts + '[' + file_name + '](' + file_name + ')' + '\n\r'

        return htmlPrefix + markdown2.markdown(scripts, extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + htmlPostfix


@app.route('/writer/<filename>')
def writer(filename):
    global htmlPrefix
    global htmlPostfix
    global siteroot
    global siteimages
    global sitemarkdown

    sethtmlbasis()
    if (path.exists(siteroot + siteimages + filename)):
        if filename[-3:] in {"png", "jpg", "gif"}:
            return send_from_directory(siteroot + siteimages, filename)

    if path.exists(siteroot + sitemarkdown + filename):
        if filename[-3:] == ".md":
            with open(siteroot + sitemarkdown + filename) as f:
                read_data = f.read()

            return htmlPrefix + "<br><h6><a href='http://localhost:7000/editmarkdown/" + filename + "'>edit " + filename + "</a></h6><br>" + markdown2.markdown(read_data, extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + htmlPostfix

    return htmlPrefix + markdown2.markdown('*404* NOTFOUND\n\r', extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + "<br><h6><a href='http://localhost:7000/createnewmarkdown/" + filename + "'>create " + filename + "</a></h6><br>" + htmlPostfix


if __name__ == '__main__':
    sethtmlbasis()
    app.run(port=7000)
