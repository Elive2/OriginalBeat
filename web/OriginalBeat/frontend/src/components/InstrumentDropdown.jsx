import React from 'react';
import '../index.css';

import '@progress/kendo-theme-default/dist/all.css';
import {DropDownList} from '@progress/kendo-react-dropdowns';




class InstrumentDropdown extends React.Component {
	constructor(props) {
	  super(props);
	}
	instrument = ['Synth' , 'Piano', 'Bass'];
	roll = [''];
	state = { instrument: 'Synth',
					roll: this.props.roll
				} ;

    handleChange = (event) => {
        this.setState ({
            instrument: event.target.value
        }, () => {
			var iframe = document.getElementById(this.state.roll);
			var innerDoc1 = iframe.contentDocument || iframe.contentWindow.document;

			// innerDoc1.SoundSelection.setInstrument(this.state.instrument);
			// innerDoc1.SoundSelection.onInstrument._piano.click();
			innerDoc1.getElementById(this.state.instrument).click();
		});


	}


	render() {
		return (
            <div>
                <div>Sound Selection: </div>
                <DropDownList
                    data={this.instrument}
                    value={this.state.instrument}
                    onChange={this.handleChange}
                />
            </div>
        );
	}
}
export default InstrumentDropdown
