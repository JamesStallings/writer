from flask import Flask, request, redirect, url_for, send_from_directory
import glob
import markdown2
import mf2py
from os import path

app = Flask(__name__, static_url_path='')
currentresource = ""
cssstate = "day"
css = ""
htmlPrologue = ""
htmlEpilogue = ""

""" siteroot = "site/"
siteimages = "images/"
sitemarkdown = "markdown/" """

siteroot = "./site/"
siteimages = ""
sitemarkdown = ""

cssday = """
table {
    font-size: 15px;
    table-layout: fixed;
    border-collapse: collapse;
    border: 1px solid grey;
}

tr:nth-child(odd) {
    background: #DDD7EF;
    width: auto;
    height: 40px;
    border-collapse: collapse;
    border: 1px solid grey;
    padding: 3px;
    padding-left: 5px;
    text-align: center;
}

tr:nth-child(even) {
    background: #CFCDF2;
    width: auto;
    height: 40px;
    border-collapse: collapse;
    border: 1px solid grey;
    padding: 3px;
    padding-left: 5px;
    text-align: center;
}

td:nth-child(1) {
    width: auto;
    border-collapse: collapse;
    border: 1px solid grey;
    padding: 1px;
    text-align: left;
}

td:nth-child(2) {
    width: auto;
    border-collapse: collapse;
    border: 1px solid grey;
    padding: 3px;
    padding-left: 15px;
    padding-right: 25px;
    text-align: center;
}

td:nth-child(3) {
    width: auto;
    border-collapse: collapse;
    border: 1px solid grey;
    padding: 1px;
    text-align: center;
}

td:nth-child(4) {
    width: auto;
    border-collapse: collapse;
    border: 1px solid grey;
    padding: 3px;
    padding-left: 15px;
    padding-right: 25px;
    text-align: center;
}
body {
    margin: 0 auto;
    max-width: 50em;
    font-family: "Helvetica", "Arial", sans-serif;
    line-height: 1.5;
    padding: 4em 1em;
    background: #F0F7FB;
    color: #343b82;
    overflow-x: hidden;
}

h2 {
    margin-top: 1em;
    padding-top: 1em;
}

h1, h2, strong {
    color: 333;
}

code, pre {
    background: #e5e7f9;
    border-bottom: 1px solid #d8dee9;
    color: #a7adba;
}

code {
    padding: 2px 4px;
    vertical-align: text-bottom;
}

pre {
    padding: 1em;
    border-left: 2px solid #69c;
}

a {
    color: #FF0871;
}

a:hover {
    color: #FFF823;
}

a:active {
    color: #FC0060;
}

a:visited {
    color: #4B2BFF;
}

img {
    width: 275px;
    height: 400px;
}

.modal-window {
  position: fixed;
  background-color: rgba(200, 200, 200, 0.75);
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 999;
  opacity: 0;
  pointer-events: none;
  -webkit-transition: all 0.3s;
  -moz-transition: all 0.3s;
  transition: all 0.3s;
}

.modal-window:target {
  opacity: 1;
  pointer-events: auto;
}

.modal-window>div {
  width: 400px;
  position: relative;
  margin: 10% auto;
  padding: 2rem;
  background: #fff;
  color: #444;
}

.modal-window header {
  font-weight: bold;
}

.modal-close {
  color: #aaa;
  line-height: 50px;
  font-size: 80%;
  position: absolute;
  right: 0;
  text-align: center;
  top: 0;
  width: 70px;
  text-decoration: none;
}

.modal-close:hover {
  color: #000;
}

.modal-window h1 {
  font-size: 150%;
  margin: 0 0 15px;
}
"""

cssnight = """

table {
    font-size: 15px;
    table-layout: fixed;
    border-collapse: collapse;
    border: 1px solid grey;
}

tr:nth-child(odd) {
    background: #1D172F;
    width: auto;
    height: 40px;
    border-collapse: collapse;
    border: 1px solid grey;
    padding: 3px;
    padding-left: 5px;
    text-align: center;
}

tr:nth-child(even) {
    background: #0F0D22;
    width: auto;
    height: 40px;
    border-collapse: collapse;
    border: 1px solid grey;
    padding: 3px;
    padding-left: 5px;
    text-align: center;
}

td:nth-child(1) {
    width: auto;
    border-collapse: collapse;
    border: 1px solid grey;
    padding: 1px;
    text-align: left;
}

td:nth-child(2) {
    width: auto;
    border-collapse: collapse;
    border: 1px solid grey;
    padding: 3px;
    padding-left: 15px;
    padding-right: 25px;
    text-align: center;
}

td:nth-child(3) {
    width: auto;
    border-collapse: collapse;
    border: 1px solid grey;
    padding: 1px;
    text-align: center;
}

td:nth-child(4) {
    width: auto;
    border-collapse: collapse;
    border: 1px solid grey;
    padding: 3px;
    padding-left: 15px;
    padding-right: 25px;
    text-align: center;
}
body {
    margin: 0 auto;
    max-width: 50em;
    font-family: "Helvetica", "Arial", sans-serif;
    line-height: 1.5;
    padding: 4em 1em;
    background: #0F0810;
    color: #B3A0A3;
    overflow-x: hidden;
}

textarea {
    background: #121220;
    color: #C3B0B3;
}   

hr {
    color: #22F
}

h2 {
    margin-top: 1em;
    padding-top: 1em;
}

h1, h2, h3, h4, h5, h6 strong {
    color: #A37063;
}

code, pre {
    background: #e5e7f9;
    border-bottom: 1px solid #d8dee9;
    color: #a7adba;
}

code {
    padding: 2px 4px;
    vertical-align: text-bottom;
}

pre {
    padding: 1em;
    border-left: 2px solid #69c;
}

a {
    color: #F88078;
}

a:hover {
    color: #FF8078;
}

a:active {
    color: #FF6070;
}

a:visited {
    color: #8B6B7F;
}

img {
    width: 275px;
    height: 400px;
}


.modal-window {
  position: fixed;
  background-color: rgba(20, 20, 20, 0.5);
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 999;
  opacity: 0;
  pointer-events: none;
  -webkit-transition: all 0.3s;
  -moz-transition: all 0.3s;
  transition: all 0.3s;
}

.modal-window:target {
  opacity: 1;
  pointer-events: auto;
}

.modal-window>div {
  width: 400px;
  position: relative;
  margin: 10% auto;
  padding: 2rem;
  background: #222;
  color: #888;
}

.modal-window header {
  font-weight: bold;
}

.modal-close {
  color: #333;
  line-height: 50px;
  font-size: 80%;
  position: absolute;
  right: 0;
  text-align: center;
  top: 0;
  width: 70px;
  text-decoration: none;
}

.modal-close:hover {
  color: #EEF;
}

.modal-window h1 {
  font-size: 150%;
  margin: 0 0 15px;
}
"""

css = cssday

def sethtmlbasis():
    global htmlPrologue
    global htmlEpilogue

    htmlPrologue = """
<!DOCTYPE html>
<html>
  <head>
    <title>writer markdown service 0.1a</title>
    <style type=text/css>""" + css + """</style>
  </head>
  <body>
"""

    htmlEpilogue = """
    <footer>
      <h6>A complete <a href="https://www.markdownguide.org/basic-syntax/" target="top">markdown reference</a> is available</h6>
      <h6><a href="#open-modal">system menu</a></h6>
      <div id="open-modal" class="modal-window">
        <div>
          <a href="#modal-close" title="close" class="modal-close">close &times;</a>
          <h1>system menu</h1>
          <div><a href='http://localhost:7000/togglecss'>toggle CSS<div>
          <div><a href='http://localhost:7000/importhcard/'>import hcard.html<div>
        </div>
      </div>
    </footer>
  </body>
</html>
"""


def redirect_url():
    return request.args.get('next') or request.referrer or url_for('index')


@app.route('/togglecss', methods=['GET'])
def togglecss():
    global cssstate
    global css
    global htmlPrologue
    global htmlEpilog

    if cssstate == "day":
        cssstate = "night"
        css = cssnight
    else:
        cssstate = "day"
        css = cssday

    sethtmlbasis()
    return redirect(redirect_url())

@app.route('/importhcard', methods=['GET'])
def importhcard():
    global hcard

    with open('hcard.html','r') as file:
        hcard = mf2py.parse(doc=file)
    
    
@app.route('/writemarkdown', methods=['POST'])
def writemarkdown():
    global htmlPrologue
    global htmlEpilog

    if request.form['submit'] == 'cancel':
        return redirect('http://localhost:7000/writer/' + request.form['filename'])
    elif request.form['submit'] == 'done':
        file_name = siteroot + sitemarkdown + request.form['filename']
        f = open(file_name, 'w')
        f.write(request.form['markdowntxt'])
        f.close()
        return redirect('http://localhost:7000/writer/' + request.form['filename'])
        

@app.route('/writenewmarkdown/<filename>', methods=['GET'])
def writenewmarkdown(filename):
    global htmlPrologue
    global htmlEpilog

    return htmlPrologue + """
<form method='POST' action="/writemarkdown" role='form'>
<textarea id='markdowntxt' name='markdowntxt' rows='32' cols='120'>
""" + "be somebody" + """
</textarea>
<br>
<input type="hidden" name="filename" value=""" + filename + """>
<input type='submit' name='submit' value='done'>
<input type='submit' name='submit' value='cancel'>
</form>
""" + htmlEpilogue


@app.route('/editmarkdown/<filename>', methods=['GET'])
def editmarkdown(filename):
    global htmlPrologue
    global htmlEpilog

    file_name = siteroot + sitemarkdown + filename
    if path.exists(file_name):
        with open(file_name) as f:
            read_data = f.read()
            f.close()

        return htmlPrologue + """
<form method='POST' action="/writemarkdown" role='form'>
<textarea id='markdowntxt' name='markdowntxt' rows='32' cols='120'>
""" + read_data + """
</textarea>
<br>
<input type="hidden" name="filename" value=""" + filename + """>
<input type='submit' name='submit' value='done'>
<input type='submit' name='submit' value='cancel'>
</form>
""" + htmlEpilogue
    else:
        return htmlPrologue + markdown2.markdown('*404* NOTFOUND\n\r',extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + htmlEpilogue


@app.route('/writer/')
def renderdefaultview():
    global htmlPrologue
    global htmlEpilog
    global siteroot
    global sitemarkdown

    if path.exists(siteroot + sitemarkdown + 'index.md'):
        with open(siteroot + sitemarkdown + 'index.md') as f:
            read_data = f.read()

        return htmlPrologue + "<br><h6><a href='http://localhost:7000/editmarkdown/index.md'>edit index.md</a></h6><br>" + markdown2.markdown(read_data, extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + htmlEpilogue
    else:
        scripts = ""
        for file_name in glob.iglob('./*.md', recursive=True):
            scripts = scripts + '[' + file_name + '](' + file_name + ')' + '\n\r'

        return htmlPrologue + markdown2.markdown(scripts, extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + htmlEpilogue


@app.route('/exporthtml/')
def exporthtml():
    global htmlPrologue
    global htmlEpilogue
    global currentresource 
    
    filename = './' + currentresource.split('/')[2]

    print('filename. %s' % filename)
    if path.exists(filename):
        with open(filename) as f:
            read_data = f.read()

        sethtmlbasis()

        htmlfile = filename + ".html"

        with open(htmlfile, 'w') as newf:
            write_data = newf.write(htmlPrologue + "<br><h6><a href='http://localhost:7000/editmarkdown/" + filename + "'>edit " + filename + "</a></h6><br>" + markdown2.markdown(read_data, extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + htmlEpilogue)

        return htmlPrologue + "<br><h6><a href='http://localhost:7000/editmarkdown/" + filename + "'>edit " + filename + "</a></h6><br>" + markdown2.markdown(read_data, extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + htmlEpilogue


@app.route('/writer/<filename>')
def writer(filename):
    global htmlPrologue
    global htmlEpilogue
    global siteroot
    global siteimages
    global sitemarkdown

    if (path.exists(siteroot + siteimages + filename)):
        if filename[-3:] in {"png", "jpg", "gif"}:
            return send_from_directory(siteroot + siteimages, filename)

    if path.exists(siteroot + sitemarkdown + filename):
        if filename[-3:] == ".md":
            with open(siteroot + sitemarkdown + filename) as f:
                read_data = f.read()

            return htmlPrologue + "<br><h6><a href='http://localhost:7000/editmarkdown/" + filename + "'>edit " + filename + "</a></h6><br>" + markdown2.markdown(read_data, extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + htmlEpilogue

    return htmlPrologue + markdown2.markdown('*404* NOTFOUND\n\r', extras=["footnote","strike","tables","code-color","code-friendly","cuddled-lists","fenced-code-blocks"]) + "<br><h6><a href='http://localhost:7000/writenewmarkdown/" + filename + "'>create " + filename + "</a></h6><br>" + htmlEpilogue


if __name__ == '__main__':
    sethtmlbasis()
    app.run(port=7000)
