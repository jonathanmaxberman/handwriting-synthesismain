
#from io import RawIOBase
import numpy as np
#import drawing
import json
from drawing import align, denoise, coords_to_offsets, normalize
from ViewStrokeNPY import plot_stroke
def handle_draw_data(data, priming_sequence):
    # Decode the JSON data
    #draw_data = json.loads(data)
    print("Hello!")
    all_strokes = []
    for stroke_data in data:
        x = np.array(stroke_data["x"], dtype=np.float32)
        y = np.array(stroke_data["y"], dtype=np.float32)

        # Create a 'pen state' array, defaulting to 0 (pen down)
        pen_state = np.zeros_like(x, dtype=np.float32)

        # Set the last point of each stroke to 1 (pen up)
        pen_state[-1] = 1

        # Combine x, y, and pen state into a single array
        stroke = np.column_stack((x, y, pen_state))
        all_strokes.extend(stroke.tolist())

    strokes = np.array(all_strokes, dtype=np.float32)
    print(strokes)
    canvas_height = 200
    strokes[:, 1] = canvas_height - strokes[:, 1]

    # Process the strokes data
    strokes = align(strokes)
    strokes = denoise(strokes)
    offsets = coords_to_offsets(strokes)
    normalized_strokes = normalize(offsets)

    # Convert back to float32 and save the normalized strokes data as a .npy file
    normalized_strokes = normalized_strokes.astype(np.float32)
    print("Shape of the strokes array:", normalized_strokes.shape)
    np.save('./styles/style-16-strokes.npy', normalized_strokes)
    np.save('style-16-strokes.npy', normalized_strokes)
    print("Processed strokes data saved.")

    # Handle the priming sequence
    #print(text.value.encode('utf-8'))
    priming_sequence_bytes = priming_sequence.encode('utf-8')
    np.save('./styles/style-16-chars.npy', priming_sequence_bytes)
    print("Priming sequence saved.")

    #view the plot
    plot_stroke(normalized_strokes)
    # Download the files
    #files.download('style-14-strokes.npy')
    #files.download('style-14-chars.npy')
