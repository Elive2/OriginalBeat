//ideas for this component were taking from 
//https://codesandbox.io/s/l4jjvzmp47
//

import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import ListItemText from '@material-ui/core/ListItemText';
import ListItem from '@material-ui/core/ListItem';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import CloseIcon from '@material-ui/icons/Close';
import Slide from '@material-ui/core/Slide';
import DimensionsProvider from './DimensionsProvider';
import SoundfontProvider from './SoundfontProvider';
import RecordingPiano from './RecordingPiano'
import RollDisplay from './RollDisplay';
import {Row, Col} from 'reactstrap'
import {Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import { Piano, KeyboardShortcuts, MidiNumbers } from 'react-piano';
import 'react-piano/dist/styles.css';
import MelodyRoll from './MelodyRoll'
import { ButtonDropdown, DropdownToggle, DropdownMenu, DropdownItem } from 'reactstrap';

var server = process.env.API_URL

// webkitAudioContext fallback needed to support Safari
const audioContext = new (window.AudioContext || window.webkitAudioContext)();
const soundfontHostname = 'https://d1pzp51pvbm36p.cloudfront.net';

var CHROMATIC = [ 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B' ]

function noteFromMidi(midiNumber) {
  if (isNaN(midiNumber) || midiNumber < 0 || midiNumber > 127) return null;
  var name = CHROMATIC[midiNumber % 12];
  var oct = Math.floor(midiNumber / 12) - 1;
  return name + oct;
}


function formatMidi(midi_json) {
    //console.log("MIDI JSON")
    //console.log(midi_json)
    var formattedHeader = {tempo: 120, timeSignature: [4,4]};
    var formattedNotes = [];

    for(var i = 0; i < midi_json.length; i++) {
        var newNote = {'time': midi_json[i].time.toString() + 'i',
                    'midiNote': midi_json[i].midiNumber,
                    'note': noteFromMidi(midi_json[i].midiNumber),
                    'velocity': 1,
                    'duration': midi_json[i].duration.toString() + 'i',
                };
        formattedNotes.push(newNote);
    }
    // for(var i = 0; i < midi_json['tracks'][1]['notes'].length; i++) {
    //     var oldNote = midi_json['tracks'][1]['notes'][i]
    //     var newNote = {'time': (Math.floor(oldNote['ticks'] / 20)).toString() + 'i',
    //                 'midiNote': oldNote['midi'],
    //                 'note': noteFromMidi(oldNote['midi']),
    //                 'velocity': 1,
    //                 'duration': (Math.floor(oldNote['durationTicks'] / 20)).toString() + 'i',
    //             };
    //     formattedNotes.push(newNote);
    // }
    var formattedMidi = {header: formattedHeader, notes: formattedNotes};

    return formattedMidi;
}

const noteRange = {
  first: MidiNumbers.fromNote('c3'),
  last: MidiNumbers.fromNote('f5'),
};
const keyboardShortcuts = KeyboardShortcuts.create({
  firstNote: noteRange.first,
  lastNote: noteRange.last,
  keyboardConfig: KeyboardShortcuts.HOME_ROW,
});

const styles = {
  appBar: {
    position: 'relative',
  },
  flex: {
    flex: 1,
  },
};

function Transition(props) {
  return <Slide direction="up" {...props} />;
}


class PianoInput extends React.Component {


  constructor(props) {
    super(props);

    this.state = {
      model: 'KeyChord2',
      dropdownOpen: false,
      modal: false,
      open: false,
      recording: {
        mode: 'RECORDING',
        events: [],
        currentTime: 0,
        currentEvents: [],
      },
    };

    this.scheduledEvents = [];
  }

  getRecordingEndTime = () => {
    if (this.state.recording.events.length === 0) {
      return 0;
    }
    return Math.max(
      ...this.state.recording.events.map(event => event.time + event.duration),
    );
  };

  setRecording = value => {
    this.setState({
      recording: Object.assign({}, this.state.recording, value),
    });
  };

  onClickPlay = () => {
    this.setRecording({
      mode: 'PLAYING',
    });
    const startAndEndTimes = _.uniq(
      _.flatMap(this.state.recording.events, event => [
        event.time,
        event.time + event.duration,
      ]),
    );
    startAndEndTimes.forEach(time => {
      this.scheduledEvents.push(
        setTimeout(() => {
          const currentEvents = this.state.recording.events.filter(event => {
            return event.time <= time && event.time + event.duration > time;
          });
          this.setRecording({
            currentEvents,
          });
        }, time * 1000),
      );
    });
    // Stop at the end
    setTimeout(() => {
      this.onClickStop();
    }, this.getRecordingEndTime() * 1000);
  };

  onClickStop = () => {
    this.scheduledEvents.forEach(scheduledEvent => {
      clearTimeout(scheduledEvent);
    });
    this.setRecording({
      mode: 'RECORDING',
      currentEvents: [],
    });
  };

  onClickClear = () => {
    this.onClickStop();
    this.setRecording({
      events: [],
      mode: 'RECORDING',
      currentEvents: [],
      currentTime: 0,
    });
  };

  handleClickOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
    this.onClickClear()
  };

  handleSave = () => {
    this.setState({
      open: false
    })

    this.setState({
      modal: true
    })
  }

  handleUpload = () => {
    fetch(server + 'inputmidi/', {
      method: 'post',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'midi':this.state.recording.events, 'model':this.state.model})
    }).then(() => {
      window.location.replace(server + 'project/')
    })
      .catch((error) => {
      console.log(error)
    })

    this.setState({
      modal: false,
      open: false
    })

  }

  toggle = (prevState) => {
    this.setState({
      modal: !prevState
    });
    this.onClickClear()
  }

  toggleDropdown = (prevState) => {
    this.setState({
      dropdownOpen: !this.state.dropdownOpen
    });
  }

  refreshNotes = () => {
    this.setState({
      midi: this.formatMidi(this.state.recording.events),
    })
  }

  selectDropdown(select_model)  {
    this.setState({
      model:select_model
    })
  }

  render() {
    const { classes } = this.props;
    return (
      <div>
        <Modal isOpen={this.state.modal} toggle={this.toggle}>
          <ModalHeader toggle={this.toggle}>Upload Melody</ModalHeader>
          <ModalBody>
            <Row>
              <Col>
                {this.state.recording.events.length > 0 &&
                  <MelodyRoll midi={formatMidi(this.state.recording.events)}/>
                }
              </Col>
            </Row>
            <Row>
              <Col>
                <ButtonDropdown isOpen={this.state.dropdownOpen} toggle={this.toggleDropdown}>
                  <DropdownToggle caret>
                    Select Generation Model
                  </DropdownToggle>
                  <DropdownMenu>
                    <DropdownItem onClick={() => {this.selectDropdown('KeyChord')}}>KeyChord</DropdownItem>
                    <DropdownItem onClick={() => {this.selectDropdown('KeyChord2')}}>KeyChord2</DropdownItem>
                    <DropdownItem onClick={() => {this.selectDropdown('BayesNet')}}>Bayesian Network</DropdownItem>
                  </DropdownMenu>
                </ButtonDropdown>
              </Col>
              <Col>
                {this.state.model}
              </Col>
            </Row>
          </ModalBody>
          <ModalFooter>
            <Button color="primary" onClick={this.handleUpload}>Upload</Button>
          </ModalFooter>
        </Modal>
        <Button variant="outlined" color="primary" onClick={this.handleClickOpen}>
          Piano Editor
        </Button>
        <Dialog
          fullScreen
          open={this.state.open}
          onClose={this.handleClose}
          TransitionComponent={Transition}
        >
          <AppBar id="piano-input">
            <Toolbar>
              <IconButton color="inherit" onClick={this.handleClose} aria-label="Close">
                <CloseIcon />
              </IconButton>
              <Typography variant="h6" color="inherit" className={classes.flex}>
                Sound
              </Typography>
              <Button color="inherit" onClick={this.handleSave}>
                save
              </Button>
            </Toolbar>
          </AppBar>
            <br/>
            <br/>
            <br/>
            <Row>
              <Col>
                <br/>
                <br/>
                <br/>
                  <RollDisplay data={this.state.recording.events}/>
                
                <DimensionsProvider>
                  {({ containerWidth, containerHeight }) => (
                    <SoundfontProvider
                      instrumentName="acoustic_grand_piano"
                      audioContext={audioContext}
                      hostname={soundfontHostname}
                      render={({ isLoading, playNote, stopNote }) => (
                        <RecordingPiano
                          recording={this.state.recording}
                          setRecording={this.setRecording}
                          noteRange={noteRange}
                          width={containerWidth}
                          playNote={playNote}
                          stopNote={stopNote}
                          disabled={isLoading}
                          keyboardShortcuts={keyboardShortcuts}
                          {...this.props}
                        />
                      )}
                    />
                  )}
                </DimensionsProvider>
              </Col>
            </Row>
        </Dialog>
      </div>
    );
  }
}

PianoInput.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(PianoInput);