!function(e){function t(o){if(n[o])return n[o].exports;var r=n[o]={exports:{},id:o,loaded:!1};return e[o].call(r.exports,r,r.exports,t),r.loaded=!0,r.exports}var o=window.webpackJsonp;window.webpackJsonp=function(n,i){for(var a,l,s=0,c=[];s<n.length;s++)l=n[s],r[l]&&c.push.apply(c,r[l]),r[l]=0;for(a in i)Object.prototype.hasOwnProperty.call(i,a)&&(e[a]=i[a]);for(o&&o(n,i);c.length;)c.shift().call(null,t)};var n={},r={1:0};return t.e=function(e,o){if(0===r[e])return o.call(null,t);if(void 0!==r[e])r[e].push(o);else{r[e]=[o];var n=document.getElementsByTagName("head")[0],i=document.createElement("script");i.type="text/javascript",i.charset="utf-8",i.async=!0,i.src=t.p+"../../../static/"+e+".js",n.appendChild(i)}},t.m=e,t.c=n,t.p="",t(0)}([function(e,t,o){function n(e){if(isNaN(e)||e<0||e>127)return null;var t=a[e%12],o=Math.floor(e/12)-1;return t+o}function r(e){console.log("formating the midi file for pianoroll");for(var t={tempo:64,timeSignature:[4,4]},o=[],r=0;r<e.tracks[0].notes.length;r++)oldNote=e.tracks[0].notes[r],newNote={time:oldNote.ticks.toString()+"i",midiNote:oldNote.midi,note:n(oldNote.midi),velocity:1,duration:oldNote.durationTicks.toString()+"i"},o.push(newNote);var i={header:t,notes:o};return i}var i="http://127.0.0.1:8000/midi/",a=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"];o.e(0,function(e){var t=[e(61),e(46),e(50),e(40),e(4),e(67),e(54),e(71),e(1),e(41),e(42),e(53)];(function(e,t,o,n,a,l,s,c,d,u,p,f){e(function(){var e=new o,c=new t(document.body),m=new n(document.body);new p(document.body,c,m);f.fromUrl(i).then(function(e){console.log("MIDI NAME"),final_mid=r(e),console.log("FORMATTED MIDI"),console.log(final_mid),c.setScore(final_mid)});console.log(l),m.onInstrument(function(t){e.setInstrument(t)}),m.onPlay(function(t){t?(d.context.resume(),c.start()):(c.stop(),e.releaseAll())}),m.onScore(function(e){c.setScore(e)}),c.onnote=function(t,o,n,r){e.triggerAttackRelease(t,o,n,r)},c.onstop=function(){e.releaseAll()};new u(function(){a.stop(),c.stop(),m.stop()});window.parent.postMessage("loaded","*");var w=/iPad|iPhone|iPod/.test(navigator.userAgent)&&!window.MSStream;if(w){var g=document.createElement("div");g.id="iOSTap",document.body.appendChild(g),new s(d.context,g).then(function(){g.remove(),window.parent.postMessage("ready","*")})}else window.parent.postMessage("ready","*")})}).apply(null,t)})}]);