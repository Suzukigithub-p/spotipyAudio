# app.py

from flask import Flask, request,render_template
from modules import spotipyAudio


app = Flask(__name__)
spA = spotipyAudio.spotipyAudio()

tasks = []
@app.route('/search')
def entry()-> str:
    return render_template('entry.html',the_title="search")

@app.route('/trackAnalysis', methods=["POST"])
def trackAnalysis()-> str:
    url=request.form['URL']
    trackFeature=spA.trackAnalysis([url])
    return render_template('trackAnalysis.html',the_title="result",the_result=trackFeature[0])

@app.route('/playlistAnalysis', methods=["POST"])
def playlistAnalysis()-> str:
    url=request.form['URL']
    playlistFeatures,keysSum=spA.playlistAnalysis([url])
    html="<table><p>search</p>"
    for track in playlistFeatures["track"]: html+='<tr><td>'+str(track)+'</td></tr>\n'
    html+="</table>"
    return render_template('playlistAnalysis.html',the_title="result",html=html,playlistName=playlistFeatures["playlistName"],keysSum=keysSum)


if __name__ == '__main__':
    app.run(debug=True)
