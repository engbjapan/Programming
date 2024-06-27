from midiutil import MIDIFile # pip install midiutil

# Create a MIDI file with one track
midi = MIDIFile(1)

# Track, time, and tempo settings
track = 0
time = 0
tempo = 120

midi.addTempo(track, time, tempo)

# Define the melody with duration
melody = [
    ('D3', 1), ('D3', 1), ('E3', 1), ('F3', 1), ('G3', 1), ('A3', 1), ('A3', 1), ('C4', 1),
    ('G3', 1), ('F3', 1), ('G3', 1), ('G3', 1), ('A3', 1), ('F3', 1), ('E3', 1), ('F3', 1), ('E3', 1), ('D3', 1)
]

# Note-to-MIDI conversion
note_to_midi = {
    'C3': 48, 'C#3': 49, 'D3': 50, 'D#3': 51, 'E3': 52, 'F3': 53, 'F#3': 54, 'G3': 55, 'G#3': 56, 'A3': 57, 'A#3': 58, 'B3': 59,
    'C4': 60, 'C#4': 61, 'D4': 62, 'D#4': 63, 'E4': 64, 'F4': 65, 'F#4': 66, 'G4': 67, 'G#4': 68, 'A4': 69, 'A#4': 70, 'B4': 71
}

# Add notes to the MIDI file
for note, duration in melody:
    midi.addNote(track, 0, note_to_midi[note], time, duration, 100)
    time += duration

# Save the MIDI file
midi_path = "melody.mid"
with open(midi_path, "wb") as output_file:
    midi.writeFile(output_file)

print(f"MIDI file saved as {midi_path}")
