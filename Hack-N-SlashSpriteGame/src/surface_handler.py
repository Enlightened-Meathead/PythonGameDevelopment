import pygame

class SpriteSurface():
    def __init__(self, sprite_sheet,
                 num_of_frames,
                 frame_width,
                 frame_height,
                 scale=1,
                 x_center_offset=0,
                 crop_top=0,
                 crop_right=0,
                 crop_bottom=0,
                 crop_left=0):
        self.sprite_sheet = pygame.image.load(sprite_sheet) # Surface with all sprites in a sheet
        self.num_of_frames = num_of_frames
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale # How big the frame is

        # Crop values to remove empty space from hitbox and center image if sprite isnt centered on frame
        self.x_center_offset = x_center_offset
        self.crop_top = crop_top
        self.crop_right = crop_right
        self.crop_bottom = crop_bottom
        self.crop_left = crop_left

        self.current_frame = 0
        self.current_frame_image = self.get_frame(0) # Subsurface of the current frame
        self.tick_of_last_animation = 0 # What game tick in ms did the last frame occur

    # Return the subsurface of the sprite surface
    def get_frame(self, frame):
        # If the frame changes, update the tick
        if frame != self.current_frame:
            self.tick_of_last_animation = pygame.time.get_ticks()
            self.current_frame = frame

        # Calculate where to start the subsection
        x_start = ((self.current_frame * self.frame_width) + self.x_center_offset) + self.crop_left
        y_start = 0 + self.crop_top

        # calculate how much of the image to trim
        x_length = self.frame_width - self.crop_left - self.crop_right
        y_length = self.frame_height - self.crop_top - self.crop_bottom

        subsurface = self.sprite_sheet.subsurface(x_start, y_start, x_length, y_length)

        # Store the subsurface based on the frame
        self.current_frame_image = pygame.transform.scale_by(subsurface, self.scale)

        return self.current_frame_image

    def get_next_frame(self):
        next_frame = self.current_frame + 1
        # Loop back to first frame if the last frame is present
        if next_frame > self.num_of_frames - 1:
            next_frame = 0
        return self.get_frame(next_frame)

    def run_animation(self, milliseconds, loop = False):
        if pygame.time.get_ticks() - self.tick_of_last_animation < milliseconds or (not loop and self.num_of_frames - 1 == self.current_frame):
            return self.current_frame_image
        else:
            return self.get_next_frame()



