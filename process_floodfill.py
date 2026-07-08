from PIL import Image

def process_logo(input_path, output_path, tolerance=10):
    img = Image.open(input_path).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    # Get background colors from the 4 corners
    corners = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
    # Use the top-left corner as the primary background color
    bg_color = pixels[0, 0]
    
    def color_distance(c1, c2):
        # Manhattan distance for RGB
        return sum(abs(a - b) for a, b in zip(c1[:3], c2[:3]))
    
    # BFS to find all contiguous background pixels from the edges
    queue = []
    visited = set()
    
    # Start from all edges to be safe
    for x in range(width):
        queue.append((x, 0))
        queue.append((x, height - 1))
    for y in range(height):
        queue.append((0, y))
        queue.append((width - 1, y))
        
    for pt in queue:
        visited.add(pt)
        
    to_transparent = []
    
    while queue:
        x, y = queue.pop(0)
        current_color = pixels[x, y]
        
        # If it's close to the background color, it's background
        if color_distance(current_color, bg_color) <= tolerance:
            to_transparent.append((x, y))
            
            # Add neighbors
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))

    # Apply transparency
    for x, y in to_transparent:
        pixels[x, y] = (0, 0, 0, 0)
        
    img.save(output_path, "PNG")
    print(f"Successfully removed background using flood fill: {output_path}")

try:
    process_logo("logo.jpg", "logo.png")
except Exception as e:
    print(f"Error: {e}")
