; Setup constants to make code less redundant and more legible
PPUCTRL   = $2000           ; Writes PPU control flags
PPUMASK   = $2001           ; Writes PPU mask flags
PPUSTATUS = $2002           ; Reads PPU action flags and resets PPUADDR
OAMADDR   = $2003           ; Points to where in OAM we write to
PPUSCROLL = $2005           ; Handles where the PPU scroll lines are
PPUADDR   = $2006           ; Stores an address (hi then lo byte) to PPU
PPUDATA   = $2007           ; Writes data to and increments said PPUADDR
OAMDMA    = $4014           ; Receives address to transfer mempage to OAM
P1CONTROL = $4016           ; Latch address for player 1's controller

; Bytemapped player inputs (MUST FOLLOW A HASH [#], THESE ARE INSTANTS)
BTN_RIGHT = %00000001 
BTN_LEFT  = %00000010
BTN_DOWN  = %00000100
BTN_UP    = %00001000
; The rest remain unused in the meantime, so they have been commented out
; BTN_START = %00010000
; BTN_SELCT = %00100000
; BTN_B     = %01000000
; BTN_A     = %10000000



.segment "HEADER"
.byte $4E, $45, $53, $1A    ; iNES magic word
.byte $02                   ; Number of 16KB PRG-ROM banks
.byte $01                   ; Number of 8KB CHR-ROM banks
.byte %00000001             ; Vertical mirroring, no save RAM, no mapper
.byte %00000000             ; No special-case flags or mapper
.byte $00                   ; No PRG-RAM
.byte $00                   ; NTSC



.segment "ZEROPAGE"
player_x: .res 1            ; Player x-position
player_y: .res 1            ; Player y-position
player_d: .res 1            ; Player sprite offset for direction
player_s: .res 1            ; Player sprite offset for animation state
anim_cnt: .res 1            ; Animation count clock that player_s uses
oam_slot: .res 1            ; Offset to change where in OAM to write
p1_btns:  .res 1            ; Bytes that deal with player 1's movement



.segment "RODATA"
palettes:
; First set of palettes (TODO: Add second set for second stage)
.byte $0C, $30, $0B, $0f
.byte $0C, $10, $15, $07
.byte $0C, $35, $22, $04
.byte $0C, $37, $22, $1B
.byte $0C, $27, $14, $0F
.byte $0C, $27, $14, $0F
.byte $0C, $27, $14, $0F
.byte $0C, $27, $14, $0F
sprites:
; The player's sprite data
; Each group is a direction and each subgroup of 4 is an animation frame
; Direction groups are ordered {Down, Up, Left, Right}
; Animation groups are ordered {Still, Right Leg Lean, Left Leg Lean}
.byte $00, $02, %00100000, $00
.byte $00, $03, %00100000, $08
.byte $08, $12, %00100000, $00
.byte $08, $13, %00100000, $08
.byte $00, $00, %00100000, $00
.byte $00, $01, %00100000, $08
.byte $08, $10, %00100000, $00
.byte $08, $11, %00100000, $08
.byte $00, $00, %00100000, $00
.byte $00, $01, %00100000, $08
.byte $08, $14, %00100000, $00
.byte $08, $15, %00100000, $08

.byte $00, $06, %00100000, $00
.byte $00, $07, %00100000, $08
.byte $08, $16, %00100000, $00
.byte $08, $17, %00100000, $08
.byte $00, $08, %00100000, $00
.byte $00, $09, %00100000, $08
.byte $08, $04, %00100000, $00
.byte $08, $05, %00100000, $08
.byte $00, $08, %00100000, $00
.byte $00, $09, %00100000, $08
.byte $08, $18, %00100000, $00
.byte $08, $19, %00100000, $08
; NOTE: Sideways still frames have a dummy $FF sprite since they only use 3 sprites
.byte $00, $0C, %00100000, $00
.byte $00, $0D, %00100000, $08
.byte $08, $1C, %00100000, $04
.byte $08, $FF, %00100000, $08
.byte $00, $0A, %00100000, $00
.byte $00, $0B, %00100000, $08
.byte $08, $1A, %00100000, $00
.byte $08, $1B, %00100000, $08
.byte $00, $0A, %00100000, $00
.byte $00, $0B, %00100000, $08
.byte $08, $1E, %00100000, $00
.byte $08, $1F, %00100000, $08

.byte $00, $0D, %01100000, $00
.byte $00, $0C, %01100000, $08
.byte $08, $1D, %00100000, $04
.byte $08, $FF, %00100000, $08
.byte $00, $0B, %01100000, $00
.byte $00, $0A, %01100000, $08
.byte $08, $0E, %00100000, $00
.byte $08, $1E, %01100000, $08
.byte $00, $0B, %01100000, $00
.byte $00, $0A, %01100000, $08
.byte $08, $0F, %00100000, $00
.byte $08, $1A, %01100000, $08
tiles:
; Map tiles (TODO: Somehow turn these into metatiles of themsevles)
.byte $02, $05, $06, $07, $03, $09, $0A, $0B



.segment "CODE"

.proc irq_handler
  RTI
.endproc

.proc nmi_handler
  ; Copy mempage 2 into OAM on every interrupt
  LDA #$00
  STA OAMADDR
  LDA #$02
  STA OAMDMA

  ; Read player input
  JSR p1_read

  ; OAM reads $00s as sprites so $FF the rest of it
  LDX #$00
oam_clean:
  LDA #$FF
  STA $0200,X
  INX
  CPX #$00
  BNE oam_clean

  ; Animate player (goes before draw_player since this updates the XY coords)
  JSR anim_player

  ; Specify OAM slot then aniamte
  JSR draw_player
  
  ; Fix PPUSCROLL because PPUADDR is borked and uses the same registers
  LDX #$00
  STX PPUSCROLL
  STX PPUSCROLL

  RTI
.endproc

.proc reset_handler
  ; Ignore random IRQs then clear useless BCD logic
  SEI
  CLD
  
  ; Disable audio IRQs
  LDX #$40
  STX $4017

  ; Set up the stack
  LDX #$FF
  TXS

  ; FF -> 00 to clear CTRL and MASK
  INX
  STX PPUCTRL
  STX PPUMASK
  STX $4010

  ; Wait for PPU to fully boot
  BIT PPUSTATUS
vblankwait:
  BIT PPUSTATUS
  BPL vblankwait
vblankwait2:
  BIT PPUSTATUS
  BPL vblankwait2

  ; Set defaults for all the variables
  LDA #$80
  STA player_x
  LDA #$6F
  STA player_y
  LDA #$00
  STA player_d
  STA player_s
  STA anim_cnt
  STA oam_slot
  LDA #%00000001
  STA p1_btns

  JMP main
.endproc

.proc main
  ; Clear PPUADDR
  LDX PPUSTATUS

  ; Load palette table
  LDX #$3F
  STX PPUADDR
  LDX #$00
  STX PPUADDR
load_palettes:
  LDA palettes,X
  STA PPUDATA
  INX
  CPX #$20
  BNE load_palettes

  ; Wait for PPU to boot again
vblankwait:
  BIT PPUSTATUS
  BPL vblankwait

  ; Initiate both control and mask flags
  LDA #%10010000
  STA PPUCTRL
  LDA #%00011110
  STA PPUMASK

forever:
  JMP forever
.endproc

; Draws four successive sprites from the player's sprite table
; Parameters include position (player_x, player_y), direction (player_d),
; animation state (player_s), and OAM position (oam_slot)
.proc draw_player
  ; Stack push
  PHP
  PHA
  TXA
  PHA
  TYA
  PHA

  ; Initialize counter, then load player direction and add animation state
  LDX #$00
  LDA player_d
  CLC
  ADC player_s
  TAY
load_sprites:
  ; Add OAM offset to the counter
  TXA
  CLC 
  ADC oam_slot
  TAX

  ; Add player y-coord to the sprite y-coord
  LDA sprites, Y
  CLC
  ADC player_y
  STA $0200, X
  INY
  INX

  ; Sprite ID
  LDA sprites, Y
  STA $0200, X
  INY
  INX

  ; Sprite flags
  LDA sprites, Y
  STA $0200, X
  INY
  INX

  ; Add player x-coord to the sprite x-coord
  LDA sprites, Y
  CLC
  ADC player_x
  STA $0200, X
  INY
  INX

  ; Subtract OAM offset to properly make CPX
  TXA
  SEC 
  SBC oam_slot
  TAX

  ; Have we written four sprites? If not, continue loop
  CPX #$10
  BNE load_sprites

  ; Stack pull
  PLA
  TYA
  PLA
  TXA
  PLA
  PLP
  RTS
.endproc

; Handles both player movement and animations
.proc anim_player
  ; Stack push
  PHP
  PHA

  ; Check each of the button inputs, starting with right
  ; Depending on button input, change player direction and xy coords
  LDA p1_btns
  AND #BTN_RIGHT
  BEQ left_check
  LDA #$90
  STA player_d
  INC player_x
  JMP down_check
left_check:
  LDA p1_btns
  AND #BTN_LEFT
  BEQ down_check
  LDA #$60
  STA player_d
  DEC player_x
down_check:
  LDA p1_btns
  AND #BTN_DOWN
  BEQ up_check
  LDA #$00
  STA player_d
  INC player_y
  JMP end_check
up_check:
  LDA p1_btns
  AND #BTN_UP
  BEQ end_check
  LDA #$30
  STA player_d
  DEC player_y
end_check:

  ; Ignore animation procedure and reset counter if no direction is being held
  LDA p1_btns
  AND #%00001111
  BEQ cnt_reset

  ; Increase then load animation counter
  INC anim_cnt
  LDA anim_cnt

  ; Compare counter to four possible states
  CMP #$10
  BCC frame_right
  CMP #$20
  BCC frame_mid
  CMP #$30
  BCC frame_left
  CMP #$40
  BCC frame_mid

  ; Reset counter if it reaches 40 or player isn't pressing any directions
cnt_reset:
  LDA #$00
  STA anim_cnt
  JMP frame_mid

  ; Load corresponding frame then store to player animation state
frame_right:
  LDA #$10
  JMP store_frame
frame_left:
  LDA #$20
  JMP store_frame
frame_mid:
  LDA #$00
store_frame:
  STA player_s

  ; Stack pull
  PLA
  PLP
  RTS
.endproc

; Gets player 1's inputs
.proc p1_read
  ; Stack push
  PHP
  PHA

  ; Activate player 1's latch
  LDA #$01
  STA P1CONTROL
  LDA #$00
  STA P1CONTROL

  ; Initiate shift
  LDA #%00000001
  STA p1_btns

  ; Loop until we get all button inputs
get_buttons:
  LDA P1CONTROL
  LSR A
  ROL p1_btns
  BCC get_buttons

  ; Stack pull
  PLA
  PLP
  RTS
.endproc



; Setup interrupt vector addresses at the end of the PRG-ROM, CHR-ROM and startup
.segment "VECTORS"
.addr nmi_handler, reset_handler, irq_handler
.segment "CHARS"
.incbin "sprites.chr"
.segment "STARTUP"