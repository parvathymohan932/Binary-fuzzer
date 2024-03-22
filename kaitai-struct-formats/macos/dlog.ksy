meta:
  id: dlog
  file-extension: dlog
seq:
  - id: endianness
    type: u1
    doc: 0 - little endian 1 - big endian
  - id: body
    type: body
types:
  body:
    meta:
      endian:
        switch-on: _root.endianness
        cases:
          0: le
          1: be
    seq:
      - id: header
        type: header
    instances:
      data:
        pos: header.start_of_data
        type: data
    types:
      header:
        seq:
         - id: sample_size
           -orig-id: cbSampleEntry
           type: u1
           doc: number of bytes per sample, OpenScope = 2
         - id: header_size
           -orig-id: cbHeader
           type: u2
           doc: size of this header, including endianness
         - id: start_of_data
           -orig-id: cbHeaderInFile
           type: u2
           doc: start of data, sector aligned (512 bytes)
         - id: dlog_format
           -orig-id: format
           type: u2
           enum: dlog_formats
           doc: General format of the header and potential data
         - id: dlog_version
           -orig-id: revision
           type: u4
           doc: specific header revision (within the general format)

         - id: voltage_scale
           -orig-id: voltageUnits
           type: u8
           doc: voltage scale, or divisor (units 1/V)
         - id: stop_reason
           -orig-id: stopReason
           type: u4
           enum: stop_reasons
           doc: log stop reason
         - id: sample_initial_index
           -orig-id: iStart
           type: u8
           doc: sample index of the first data sample, usually 0
         - id: num_samples
           -orig-id: actualCount
           type: u8
           doc: number of samples
         - id: sample_rate_scale
           -orig-id: sampleFreqUnits
           type: u8
           doc: sample rate scale, or divisor (units 1/(Sa/s))
         - id: raw_sample_rate
           -orig-id: uSPS
           type: u8
           doc: sample rate, Sa/s
         - id: delay_scale
           -orig-id: delayUnits
           type: u8
           doc: delay scale, or divisor (units 1/s)
         - id: raw_delay
           -orig-id: psDelay
           type: s8
           doc: delay from the start of sampling until the first sample was taken, usually 0

         - id: num_openlogger_channels
           -orig-id: cChannels
           type: u4
           if: dlog_format == dlog_formats::openlogger
           doc: number of channels per sample
         - id: openlogger_channel_map
           -orig-id: rgChannels
           type: u1
           repeat: expr
           repeat-expr: 8
           if: dlog_format == dlog_formats::openlogger
           doc: channel order

        instances:
          sample_rate:
            value: '1.0 * raw_sample_rate / sample_rate_scale'
          delay:
            value: '1.0 * raw_delay / delay_scale'
          num_channels:
            value: 'dlog_format == dlog_formats::openlogger ? num_openlogger_channels : 1'
          channel_map:
            value: 'dlog_format == dlog_formats::openlogger ? openlogger_channel_map : [0].as<u1[]>'

      data:
        seq:
        - id: samples
          type: sample
          repeat: eos
        types:
          sample:
            seq:
              - id: channel
                type:
                  switch-on: _root.body.header.sample_size
                  cases:
                    1: s1
                    2: s2
                    4: s4
                repeat: expr
                repeat-expr: _root.body.header.num_channels

enums:
  dlog_formats:
    1: openscope
    3: openlogger
  stop_reasons:
    0: normal
    1: forced
    2: error
    3: overflow
    4: unknown