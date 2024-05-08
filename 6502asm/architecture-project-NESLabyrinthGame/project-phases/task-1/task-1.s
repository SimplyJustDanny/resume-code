; Setup constants to make code less redundant and more legible
PPUCTRL   = $2000           ; Writes PPU control flags
PPUMASK   = $2001           ; Writes PPU mask flags
PPUSTATUS = $2002           ; Reads PPU action flags and resets PPUADDR
OAMADDR   = $2003           ; Points to where in OAM we write to
PPUSCROLL = $2005           ; Handles where the PPU scroll lines are
PPUADDR   = $2006           ; Stores an address (hi then lo byte) to PPU
PPUDATA   = $2007           ; Writes data to and increments said PPUADDR
OAMDMA    = $4014           ; Receives address to transfer mempage to OAM



.segment "HEADER"
.byte $4E, $45, $53, $1A    ; iNES magic word
.byte $02                   ; Number of 16KB PRG-ROM banks
.byte $01                   ; Number of 8KB CHR-ROM banks
.byte %00000001             ; Vertical mirroring, no save RAM, no mapper
.byte %00000000             ; No special-case flags or mapper
.byte $00                   ; No PRG-RAM
.byte $00                   ; NTSC



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
; Each group is a direction and each subgroup is an animation frame
; Direction groups are ordered {Down, Up, Left, Right}
; Animation groups are ordered {Right Leg Lean, Still, Left Leg Lean}
.byte $40, $00, %00100000, $60
.byte $40, $01, %00100000, $68
.byte $48, $10, %00100000, $60
.byte $48, $11, %00100000, $68
.byte $40, $02, %00100000, $78
.byte $40, $03, %00100000, $80
.byte $48, $12, %00100000, $78
.byte $48, $13, %00100000, $80
.byte $40, $00, %00100000, $90
.byte $40, $01, %00100000, $98
.byte $48, $14, %00100000, $90
.byte $48, $15, %00100000, $98

.byte $58, $08, %00100000, $60
.byte $58, $09, %00100000, $68
.byte $60, $04, %00100000, $60
.byte $60, $05, %00100000, $68
.byte $58, $06, %00100000, $78
.byte $58, $07, %00100000, $80
.byte $60, $16, %00100000, $78
.byte $60, $17, %00100000, $80
.byte $58, $08, %00100000, $90
.byte $58, $09, %00100000, $98
.byte $60, $18, %00100000, $90
.byte $60, $19, %00100000, $98

.byte $70, $0A, %00100000, $60
.byte $70, $0B, %00100000, $68
.byte $78, $1A, %00100000, $60
.byte $78, $1B, %00100000, $68
.byte $70, $0C, %00100000, $78
.byte $70, $0D, %00100000, $80
.byte $78, $1C, %00100000, $7C
.byte $70, $0A, %00100000, $90
.byte $70, $0B, %00100000, $98
.byte $78, $1E, %00100000, $90
.byte $78, $1F, %00100000, $98

.byte $88, $0B, %01100000, $60
.byte $88, $0A, %01100000, $68
.byte $90, $0E, %00100000, $60
.byte $90, $1E, %01100000, $68
.byte $88, $0D, %01100000, $78
.byte $88, $0C, %01100000, $80
.byte $90, $1D, %00100000, $7C
.byte $88, $0B, %01100000, $90
.byte $88, $0A, %01100000, $98
.byte $90, $0F, %00100000, $90
.byte $90, $1A, %01100000, $98
tiles_1:
; First row of tiles to write onto the nametable
.byte $02, $02, $05, $05, $06, $06, $07, $07
tiles_2:
; Second row of tiles to write onto the nametable
.byte $03, $03, $09, $09, $0A, $0A, $0B, $0B



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

  ; Load all of the player sprites from the sprite table
  LDX #$00
load_sprites:
  LDA sprites,X
  STA $0200,X
  INX
  CPX #$B8
  BNE load_sprites

  ; OAM reads $00s as sprites so $FF the rest of it
oam_clean:
  LDA #$FF
  STA $0200,X
  INX
  CPX #$00
  BNE oam_clean

  ; First rows of tiles
  LDA PPUSTATUS
  LDA #$22
  STA PPUADDR
  LDA #$8C
  STA PPUADDR
  LDX #$00
  LDY #$00
row_1:
  LDA tiles_1,X
  STA PPUDATA
  INX
  CPX #$08
  BNE row_1

  CPY #$01
  BEQ next
  INY
  LDA PPUSTATUS
  LDA #$22
  STA PPUADDR
  LDA #$AC
  STA PPUADDR
  LDX #$00
  JMP row_1
next:

  ; Second rows of tiles
  LDA PPUSTATUS
  LDA #$22
  STA PPUADDR
  LDA #$CC
  STA PPUADDR
  LDX #$00
  LDY #$00
row_2:
  LDA tiles_2,X
  STA PPUDATA
  INX
  CPX #$08
  BNE row_2

  CPY #$01
  BEQ end
  INY
  LDA PPUSTATUS
  LDA #$22
  STA PPUADDR
  LDA #$EC
  STA PPUADDR
  LDX #$00
  JMP row_2
end:

  ; Attribute data for the corresponding tiles
  LDA PPUSTATUS
  LDA #$23
  STA PPUADDR
  LDA #$EB
  STA PPUADDR
  LDA #$44
  STA PPUDATA
  LDA #$EE
  STA PPUDATA

  ; Fix PPUSCROLL because PPUADDR is borked and uses the same registers
  LDX #$00
  STX PPUSCROLL
  STX PPUSCROLL

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



; Setup interrupt vector addresses at the end of the PRG-ROM, CHR-ROM and startup
.segment "VECTORS"
.addr nmi_handler, reset_handler, irq_handler
.segment "CHARS"
.incbin "sprites.chr"
.segment "STARTUP"