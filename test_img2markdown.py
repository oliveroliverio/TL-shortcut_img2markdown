#!/usr/bin/env python3
import unittest
from img2markdown import prep_for_pasting


class TestPrepForPasting(unittest.TestCase):
    def test_prep_for_pasting_with_example(self):
        """Test prep_for_pasting function with the example markdown."""
        
        # Input markdown with triple backticks, first level and second level headers
        # Long string literals are exempt from line length limits
        # fmt: off
        # noqa: E501
        input_markdown = """```markdown
# Magic Words for Diffusion Models

## Cinematic Look:

- **Cinematic:** Creates the impression of a film.
- **Film grain:** Adds film grain to simulate the look of a movie.
- **Ultra realistic:** Produces an exceptionally realistic depiction.
- **Dramatic lighting:** Creates dramatic lighting conditions.

## Different Types of Shots:

- **Extreme Close-up:** A shot that is extremely close to the subject.
- **Close-up:** A shot that shows the face or a specific detail.
- **Medium Shot:** A medium shot that shows the subject from the waist up.
- **Over-the-shoulder shot:** A shot from over the shoulder of a character.
- **Long Shot:** A shot that shows the subject from a distance.
- **Establishing Shot:** A shot taken from very far away.
- **Full Shot:** A full body shot.
- **Full Body Shot:** A complete view of the body.
- **POV (Point of View) Shot:** A shot from a character's perspective.
- **Eye level Shot:** A shot at eye level.
- **High Angle Shot:** A shot from above.
- **Low Angle Shot:** A shot from below.
- **Bird's Eye Shot:** A bird's camera perspective.
- **Drone Shot:** A shot taken with a drone.
- **GoPro Shot:** A shot using a GoPro camera.
- **Fish Eye Shot:** A shot with a fish-eye lens.
- **Rule of Thirds Shot:** Composition based on the rule of thirds principle.
- **Candid Shot:** A candid, spontaneous shot.
- **Silhouette Shot:** A shot where the subject appears as a silhouette.

## Cameras with Cinematic Look:

- **Arri Alexa:** A professional film camera used in cinema.
- **Super 16:** Vintage film aesthetic using film camera using the Super 16mm format.
- **Canon Cinema EOS:** Canon camera series for professional film and cinema use.
- **Sony CineAlta:** Sony camera series for professional film and cinema use.

## Filmmakers:

- *Quentin Tarantino:* Known for his unconventional and stylized films.
- *Alfred Hitchcock:* Master of the suspense genre.
- *Martin Scorsese:* Celebrated for his direction in films like "Taxi Driver" and "The Departed."
- *Christopher Nolan:* Known for his complex and innovative films like "Inception" and "The Dark Knight."
- *Michael Bay:* Specializes in action films with visually stunning effects.
- *Wong Kar-Wai:* Famous for his stylized action films.
- *Roger Watkins:* Director of films such as "Outland" and "2010: The Year We Make Contact."
- *James Cameron:* Director of blockbusters like "Titanic" and "Avatar."

## Genres:

- **Horror**
- **Sci-Fi**
- **Fantasy**
- **Romantic**
- **Musical**
- **Animation**

## Keywords for Movements:

- **Action scene:** A scene involving dynamic movements.
- **Dynamic action:** Dynamic actions.
- **Dynamic motion:** Dynamic movement.
- **Motion Blur:** A blur effect caused by fast movements.

## Sports Photographers:

- *Essa Einerson*
- *Walter Looss Jr.*
- *Neal Leifer*

## Cameras for Action Scenes:

- **Canon EOS-1D X Mark III:** A camera well-suited for fast action scenes.
- **GoPro Hero 8 Black**
- **Sony Alpha a9 II**

## Lighting:

- **Studio lights:** Lighting systems used in studios.
- **Stage lights:** Bright lighting.
- **Neon lights:** Lights that create a vibrant and striking atmosphere.
- **Warm Water light:** That creates a cozy mood.
- **Cold Gel light:** That creates a distant or melancholic.
- **High Key Lighting:** Bright lighting with few shadows.
- **Low Key Lighting:** Dark lighting with strong shadows.
- **Front Lighting:** Flat lighting from a source in front of the subject.
- **Practical Lighting:** Lighting that simulates the light sources in the scene.
- **Motivated Lighting:** Lighting that enhances the mood or atmosphere.
- **Sunny:** Bright lighting from direct sunlight.
- **Golden hour:** The time shortly after sunrise or before sunset with warm, golden light.
- **Hazy:** Lighting in misty weather.
- **Foggy:** Lighting in foggy weather.
- **Night:** Night time lighting.
- **Afternoon:** Lighting in the afternoon.

## Emotions:

- **Angry**
- **Sad**
- **Hope**
- **Happy**
- **Surprised**
- **Scared**
- **Bored**

## Resources for this lecture

1. [Magic Words](#)
2. [Magic Words.pdf](#)
```"""
        # fmt: on

        # Expected output with the requested formatting changes
        expected_output = """### Magic Words for Diffusion Models

**Cinematic Look:**

- **Cinematic:** Creates the impression of a film.
- **Film grain:** Adds film grain to simulate the look of a movie.
- **Ultra realistic:** Produces an exceptionally realistic depiction.
- **Dramatic lighting:** Creates dramatic lighting conditions.

**Different Types of Shots:**

- **Extreme Close-up:** A shot that is extremely close to the subject.
- **Close-up:** A shot that shows the face or a specific detail.
- **Medium Shot:** A medium shot that shows the subject from the waist up.
- **Over-the-shoulder shot:** A shot from over the shoulder of a character.
- **Long Shot:** A shot that shows the subject from a distance.
- **Establishing Shot:** A shot taken from very far away.
- **Full Shot:** A full body shot.
- **Full Body Shot:** A complete view of the body.
- **POV (Point of View) Shot:** A shot from a character's perspective.
- **Eye level Shot:** A shot at eye level.
- **High Angle Shot:** A shot from above.
- **Low Angle Shot:** A shot from below.
- **Bird's Eye Shot:** A bird's camera perspective.
- **Drone Shot:** A shot taken with a drone.
- **GoPro Shot:** A shot using a GoPro camera.
- **Fish Eye Shot:** A shot with a fish-eye lens.
- **Rule of Thirds Shot:** Composition based on the rule of thirds principle.
- **Candid Shot:** A candid, spontaneous shot.
- **Silhouette Shot:** A shot where the subject appears as a silhouette.

**Cameras with Cinematic Look:**

- **Arri Alexa:** A professional film camera used in cinema.
- **Super 16:** Vintage film aesthetic using film camera using the Super 16mm format.
- **Canon Cinema EOS:** Canon camera series for professional film and cinema use.
- **Sony CineAlta:** Sony camera series for professional film and cinema use.

**Filmmakers:**

- *Quentin Tarantino:* Known for his unconventional and stylized films.
- *Alfred Hitchcock:* Master of the suspense genre.
- *Martin Scorsese:* Celebrated for his direction in films like "Taxi Driver" and "The Departed."
- *Christopher Nolan:* Known for his complex and innovative films like "Inception" and "The Dark Knight."
- *Michael Bay:* Specializes in action films with visually stunning effects.
- *Wong Kar-Wai:* Famous for his stylized action films.
- *Roger Watkins:* Director of films such as "Outland" and "2010: The Year We Make Contact."
- *James Cameron:* Director of blockbusters like "Titanic" and "Avatar."

**Genres:**

- **Horror**
- **Sci-Fi**
- **Fantasy**
- **Romantic**
- **Musical**
- **Animation**

**Keywords for Movements:**

- **Action scene:** A scene involving dynamic movements.
- **Dynamic action:** Dynamic actions.
- **Dynamic motion:** Dynamic movement.
- **Motion Blur:** A blur effect caused by fast movements.

**Sports Photographers:**

- *Essa Einerson*
- *Walter Looss Jr.*
- *Neal Leifer*

**Cameras for Action Scenes:**

- **Canon EOS-1D X Mark III:** A camera well-suited for fast action scenes.
- **GoPro Hero 8 Black**
- **Sony Alpha a9 II**

**Lighting:**

- **Studio lights:** Lighting systems used in studios.
- **Stage lights:** Bright lighting.
- **Neon lights:** Lights that create a vibrant and striking atmosphere.
- **Warm Water light:** That creates a cozy mood.
- **Cold Gel light:** That creates a distant or melancholic.
- **High Key Lighting:** Bright lighting with few shadows.
- **Low Key Lighting:** Dark lighting with strong shadows.
- **Front Lighting:** Flat lighting from a source in front of the subject.
- **Practical Lighting:** Lighting that simulates the light sources in the scene.
- **Motivated Lighting:** Lighting that enhances the mood or atmosphere.
- **Sunny:** Bright lighting from direct sunlight.
- **Golden hour:** The time shortly after sunrise or before sunset with warm, golden light.
- **Hazy:** Lighting in misty weather.
- **Foggy:** Lighting in foggy weather.
- **Night:** Night time lighting.
- **Afternoon:** Lighting in the afternoon.

**Emotions:**

- **Angry**
- **Sad**
- **Hope**
- **Happy**
- **Surprised**
- **Scared**
- **Bored**

**Resources for this lecture**

1. [Magic Words](#)
2. [Magic Words.pdf](#)"""
        # fmt: off
        # noqa: E501

        # Call the function with the input markdown
        actual_output = prep_for_pasting(input_markdown)
        
        # Compare the actual output with the expected output
        self.assertEqual(actual_output, expected_output)


if __name__ == "__main__":
    unittest.main()
