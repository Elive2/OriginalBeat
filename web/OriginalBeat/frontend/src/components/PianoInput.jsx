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

import { Piano, KeyboardShortcuts, MidiNumbers } from 'react-piano';
import 'react-piano/dist/styles.css';

// webkitAudioContext fallback needed to support Safari
const audioContext = new (window.AudioContext || window.webkitAudioContext)();
const soundfontHostname = 'https://d1pzp51pvbm36p.cloudfront.net';

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
  state = {
    open: false,
  };

  handleClickOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  render() {
    const { classes } = this.props;
    return (
      <div>
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
              <Button color="inherit" onClick={this.handleClose}>
                save
              </Button>
            </Toolbar>
          </AppBar>
            <DimensionsProvider>
              {({ containerWidth, containerHeight }) => (
                <SoundfontProvider
                  instrumentName="acoustic_grand_piano"
                  audioContext={audioContext}
                  hostname={soundfontHostname}
                  render={({ isLoading, playNote, stopNote }) => (
                    <Piano
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
        </Dialog>
      </div>
    );
  }
}

PianoInput.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(PianoInput);