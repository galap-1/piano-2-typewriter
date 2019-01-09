import sys
import time
import keyboard

PianoOffset = 60
#This is what note the low C is on the piano keyboard

#PianoKeyNoteTable = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C^', 'C#^','D^', 'D#^', 'E^', 'F^', 
#		'F#^', 'G^', 'G#^', 'A^', 'A#^', 'B^', 'C^^']
#the relevant 25 notes in order

TypingKeyLetterTable = ['z', 's', 'x', 'd', 'c', 'v', 'g', 'b', 'h', 'n', 'j', 'm', 'q', '2', 'w', '3', 'e', 'r', '5', 't', 
		'6', 'y', '7', 'u', 'i']
#the typing keyboard letters associated with the corresponding note in KeyNoteTable

from rtmidi.midiutil import open_midiinput




# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = sys.argv[1] if len(sys.argv) > 1 else None

try:
	midiin, port_name = open_midiinput(port)
except (EOFError, KeyboardInterrupt):
	sys.exit()

print("Entering main loop. Press Control-C to exit.")
try:
	timer = time.time()
	while True:
			RawMessage = midiin.get_message()

			if RawMessage:
				MidiMessage, deltatime = RawMessage
				InputNote = MidiMessage[1] - PianoOffset
				if MidiMessage[0] == 144:
					#print ('Key On ' + str(InputNote) + ' Note: ' + str(PianoKeyNoteTable[InputNote]) + ' Character: ' + 
					#	str(TypingKeyLetterTable[InputNote]))
					if 0 <= InputNote <= 24:
						keyboard.press(TypingKeyLetterTable[InputNote])
				if MidiMessage[0] == 128:
					#print ('Key Off ' + str(InputNote) + ' Note: ' + str(PianoKeyNoteTable[InputNote]) + ' Character: ' + 
					#	str(TypingKeyLetterTable[InputNote]))
					if 0 <= InputNote <= 24:
						keyboard.release(TypingKeyLetterTable[InputNote])
                        

	time.sleep(0.01)
	
except KeyboardInterrupt:
	print('')
finally:
	print("Exit.")
	midiin.close_port()
del midiin



