from flask import Flask, request, redirect, url_for, send_from_directory
import glob
import markdown2
import mf2py
from datetime import datetime, date
from os import path

app = Flask(__name__, static_url_path='')
currentresource = ""
cssstate = "day"
css = ""
htmlPrefix = ""
htmlPostfix = ""
hcardurl = "http://code4peeps.life"
hcard = dict()
scard = dict()

""" siteroot = "site/"
siteimages = "images/"
sitemarkdown = "markdown/" """

siteroot = "./site/"
siteimages = ""
sitemarkdown = ""

mdfile = ""
def readHcard():
    global hcardurl
    global hcard
    global scard
    global mdfile
    global htmlPrefix
    global htmlPostfix

    hcard = mf2py.parse(url=hcardurl)

    if 'items' in hcard:
        scard['name'] = hcard['items'][0]['properties']['name']
        scard['nickname'] = hcard['items'][0]['properties']['nickname']
        scard['photourl'] = hcard['items'][0]['properties']['photo']
        scard['org'] = hcard['items'][0]['properties']['org']
        scard['title'] = hcard['items'][0]['properties']['job-title']
        scard['role'] = hcard['items'][0]['properties']['role']
        scard['email'] = hcard['items'][0]['properties']['email']
        scard['phone'] = hcard['items'][0]['properties']['tel']
        scard['note0'] = hcard['items'][0]['properties']['note']
    else:
        scard['name'] = "Unattributed"
        scard['nickname'] = "No such."
        scard['photourl'] = "nobody.png"
        scard['org'] = "Unafilliated"
        scard['title'] = "Untitled"
        scard['role'] = "Ronin"
        scard['email'] = "mailto: ronin@mailinator.com"
        scard['phone'] = "+1.800.347.5417"
        scard['note0'] = "Functionally Anonymous"

    return

def sethtmlbasis():
    global sitemarkdown
    global htmlPrefix
    global htmlPostfix
    global hcard
    global hcardurl
    global css
    global cssstate
    global mdfile

    readHcard()

    cssfile = "writer-%s.css" % cssstate

    print("CSS file selected: %s" % cssfile)

    if path.exists(cssfile):
        with open(cssfile) as f:
            css = f.read()
        print("CSS %s read" % cssfile)

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
  </span>""" % (scard['photourl'][0], scard['name'], scard['nickname'], scard['org'], scard['title'], scard['role'], hcardurl, scard['email'], scard['phone'], scard['note0'][0])

    htmlPostfix = """
            </div>
        </article>
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
    global readHcard
    global scard

    mdfile = request.form['filename']

    sethtmlbasis()

    readHcard()

    if request.form['submit'] == 'cancel':
        return redirect('http://localhost:7000/writer/' + mdfile)
    elif request.form['submit'] == 'done':

        file_name = siteroot + sitemarkdown + mdfile
        print("Writing file %s" % file_name)
        with open(file_name, 'w') as f:
            f.write(request.form['markdowntxt'])
        print("File %s written" % file_name) 

        """ this is where h-entry information will be injected into the html. It should then be written out after sethtmlbasis
    assenbles it into the html prefix
        """

        now = datetime.now()
        datenow = date.today()
        article = request.form['articleTitle']
        summary = request.form['articleSummary']

        if not article:
            article = "Untitled"

        if not summary:
            summary = "no summary"

        print("Setting up %s, %s on %s" % (article, summary, now))
        
        htmlPrefix = htmlPrefix + "<article class='h-entry'><h1 class='p-name'>" + article
        htmlPrefix = htmlPrefix + "</h1><p>Published by <a class='p-author h-card' href='" + hcardurl
        htmlPrefix = htmlPrefix + "'>" + scard['name'][0]
        htmlPrefix = htmlPrefix + " aka " + scard['nickname'][0]
        htmlPrefix = htmlPrefix + "</a>on <time class='dt-published' datetime='" + now.strftime("%d-%m-%Y %H:%M:%S")
        htmlPrefix = htmlPrefix + "'>" + datenow.strftime("%b-%d-%Y")
        htmlPrefix = htmlPrefix + "</time></p><p class='p-summary'>" + summary
        htmlPrefix = htmlPrefix + "</p><div class='e-content'>"

        print(htmlPrefix)
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

    readHcard()

    return htmlPrefix + """
<form method='POST' action="/writemarkdown" role='form'>
<label for="articleTitle">Article Title</label>
<input type="text" name="articleTitle" id="articleTitle"></input><br>
<label for="articleSummary">Article Summary</label>
<input type="text" name="articleSummary" id="articleSummary"></input><br>
<label for="markdowntxt">Post:
<textarea id='markdowntxt' name='markdowntxt' rows='30' cols='120'>
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

    if path.exists(siteroot + sitemarkdown + filename):
        print("requested " + filename +" found")
        if filename[-3:] == ".md":
            if path.exists(siteroot + sitemarkdown + filename + ".pre"):
                with open(siteroot + sitemarkdown + filename + ".pre","r") as f:
                    htmlPrefix = f.read()
                print("Prefix read")
            else:
                print("No prefix found")
            if path.exists(siteroot + sitemarkdown + filename + ".post"):
                with open(siteroot + sitemarkdown + filename + ".pre","r") as f:
                    htmlPostfix = f.read()
                print("Postfix read")    
            else:
                print("No postfix found")

            with open(siteroot + sitemarkdown + filename) as f:
                read_data = f.read()
            print("Markdown read")

        return htmlPrefix + """
<form method='POST' action="/writemarkdown" role='form'>
<label for="articleTitle">Article Title</label>
<input type="text" name="articleTitle" id="articleTitle"></input><br>
<label for="articleSummary">Article Summary</label>
<input type="text" name="articleSummary" id="articleSummary"></input><br>
<label for="markdowntxt">Post:
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
    global hcard
    global scard
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

    if (path.exists(siteroot + siteimages + filename) and filename[-3:] != ".md"):
        print("Send Image " + filename)
        if filename[-3:] in {"png", "jpg", "gif"}:
            return send_from_directory(siteroot + siteimages, filename)

    if path.exists(siteroot + sitemarkdown + filename):
        print("requested " + filename +" found")
        if filename[-3:] == ".md":
            if path.exists(siteroot + sitemarkdown + filename + ".pre"):
                with open(siteroot + sitemarkdown + filename + ".pre","r") as f:
                    htmlPrefix = f.read()
                print("Prefix read")
            else:
                print("No prefix found")
            if path.exists(siteroot + sitemarkdown + filename + ".post"):
                with open(siteroot + sitemarkdown + filename + ".pre","r") as f:
                    htmlPostfix = f.read()
                print("Postfix read")    
            else:
                print("No postfix found")

            with open(siteroot + sitemarkdown + filename) as f:
                read_data = f.read()
            print("Markdown read")
            

            return htmlPrefix + "<br><h6><a href='http://localhost:7000/editmarkdown/" + filename + "'>edit " + filename + "</a></h6><br>" + markdown2.markdown(read_data, extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + htmlPostfix

    return htmlPrefix + markdown2.markdown('*404* NOTFOUND\n\r', extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + "<br><h6><a href='http://localhost:7000/createnewmarkdown/" + filename + "'>create " + filename + "</a></h6><br>" + htmlPostfix


if __name__ == '__main__':
    sethtmlbasis()
    app.run(port=7000)
