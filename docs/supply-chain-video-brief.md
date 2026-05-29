# ModuleWarden video brief: "The Real Supply Chain"

A creative brief and ready-to-paste prompt for generating the hero reveal video.
Works with HeyGen, Sora, Runway Gen-3, Pika, Kling, or Grok Imagine. Tool-specific
notes at the bottom.

## The idea in one line

Everyone pictures ships and containers when they hear "supply chain." Show that
the systems moving all of it run on code, and that securing that code is the new
front line.

## Master prompt (paste this)

> Cinematic 20-second reveal, dark and premium, shot like a high-end enterprise
> brand film. Open on a sweeping aerial drift over a vast container shipping port
> at blue hour: thousands of stacked multicolored containers, towering gantry
> cranes loading a cargo ship, truck headlights tracing the quay, faint sea mist.
> Cool industrial blues. Around the one-third mark, the containers and cranes begin
> to dissolve into points of glowing emerald-green light. Those points drift upward
> and reorganize into a luminous three-dimensional network of nodes and thin
> connecting lines, a living software dependency graph suspended in dark space,
> data pulses traveling along the edges. The physical port has become a network of
> code. In the final third, one node at the center flares warning-red and the red
> begins to spread along a few connections, then a clean emerald hexagonal shield
> snaps into place over the core of the network and the red retreats, the graph
> settling back to calm emerald. Hold on the shielded network. Palette: near-black
> background (#020617), emerald greens (#34d399, #10b981), one alarm red (#ef4444).
> Volumetric glow, shallow depth of field, slow confident camera motion, no people
> in close-up, no text, no logos.

## Shot list and timing

| Time | Beat | What is on screen |
|------|------|-------------------|
| 0.0 - 6.0s | The assumption | Aerial container port, cranes, cargo ship, trucks. Real, physical, industrial. |
| 6.0 - 9.0s | The dissolve | Containers break into glowing emerald particles that lift and swirl. |
| 9.0 - 15.0s | The reveal | Particles form a 3D dependency network. Data pulses along the lines. This is the "actually it is code" moment. |
| 15.0 - 18.0s | The threat | One central node flares red; red creeps along a few edges (the compromise). |
| 18.0 - 20.0s | The gate | An emerald shield locks over the core, red retreats, network calms. Security wins. |

## Style guardrails

- Mood: ominous then reassuring. Restraint over spectacle. Think Stripe or Vercel brand film, not a crypto ad.
- Motion: slow, deliberate camera. Let the morph carry the drama, not fast cuts.
- Color discipline: emerald is the hero color, used sparingly against a near-black field. Red appears once, for the compromise, then leaves.
- No text baked into the video. Overlay copy in the site so it stays editable and sharp.

## Optional on-screen text (overlay in the site, not the render)

1. (over the port) "You picture this."
2. (over the network) "It runs on this."
3. (over the shield) "Secure the code supply chain."

## Negative prompt

> text, captions, watermark, logos, brand names, cartoon, low quality, blurry,
> warped containers, distorted faces, jittery motion, oversaturated neon, lens
> flare overload, stock-footage feel

## Format

- Aspect ratio: 16:9 for the hero background. Also export 1:1 and 9:16 for social.
- Length: 15-20s. Loop-friendly is a bonus; if the tool cannot loop, render the
  calm shielded-network end state long enough to crossfade back to the port.
- Resolution: 1080p minimum for the hero. 4K if the tool supports it.

## Tool-specific notes

- HeyGen / Sora / Kling: paste the master prompt; these handle the morph best. Ask for "seamless transition, no hard cut" between the port and the network.
- Runway Gen-3: split into two generations (port, then network) and use the morph/transition tool between them for a cleaner dissolve.
- Grok Imagine: 720p, 15s max. Drop the shield beat if it crowds the time budget; the port-to-network morph is the priority.
- For a perfect loop: render forward, then mirror it in post (ffmpeg boomerang) so the end state flows back to the open.
