from enum import Enum


# ISO/IEC 14496-3 Table 1.17 – Audio Object Types
class AudioObjectType(Enum):
    MPEG4_AUDIO_OBJECT_TYPE_AAC_MAIN = 1  # AAC Main Profile                             
    MPEG4_AUDIO_OBJECT_TYPE_AAC_LC = 2  # AAC Low Complexity                           
    MPEG4_AUDIO_OBJECT_TYPE_AAC_SSR = 3  # AAC Scalable Sample Rate                     
    MPEG4_AUDIO_OBJECT_TYPE_AAC_LTP = 4  # AAC Long Term Predictor                      
    MPEG4_AUDIO_OBJECT_TYPE_SBR = 5  # Spectral Band Replication                    
    MPEG4_AUDIO_OBJECT_TYPE_AAC_SCALABLE = 6  # AAC Scalable                                 
    MPEG4_AUDIO_OBJECT_TYPE_TWINVQ = 7  # Twin VQ                                      
    MPEG4_AUDIO_OBJECT_TYPE_CELP = 8  # CELP                                         
    MPEG4_AUDIO_OBJECT_TYPE_HVXC = 9  # HVXC                                         
    MPEG4_AUDIO_OBJECT_TYPE_TTSI = 12  # TTSI                                         
    MPEG4_AUDIO_OBJECT_TYPE_MAIN_SYNTHETIC = 13  # Main Synthetic                               
    MPEG4_AUDIO_OBJECT_TYPE_WAVETABLE_SYNTHESIS = 14  # WavetableSynthesis                           
    MPEG4_AUDIO_OBJECT_TYPE_GENERAL_MIDI = 15  # General MIDI                                 
    MPEG4_AUDIO_OBJECT_TYPE_ALGORITHMIC_SYNTHESIS = 16  # Algorithmic Synthesis                        
    MPEG4_AUDIO_OBJECT_TYPE_ER_AAC_LC = 17  # Error Resilient AAC Low Complexity           
    MPEG4_AUDIO_OBJECT_TYPE_ER_AAC_LTP = 19  # Error Resilient AAC Long Term Prediction     
    MPEG4_AUDIO_OBJECT_TYPE_ER_AAC_SCALABLE = 20  # Error Resilient AAC Scalable                 
    MPEG4_AUDIO_OBJECT_TYPE_ER_TWINVQ = 21  # Error Resilient Twin VQ                      
    MPEG4_AUDIO_OBJECT_TYPE_ER_BSAC = 22  # Error Resilient Bit Sliced Arithmetic Coding 
    MPEG4_AUDIO_OBJECT_TYPE_ER_AAC_LD = 23  # Error Resilient AAC Low Delay                
    MPEG4_AUDIO_OBJECT_TYPE_ER_CELP = 24  # Error Resilient CELP                         
    MPEG4_AUDIO_OBJECT_TYPE_ER_HVXC = 25  # Error Resilient HVXC                         
    MPEG4_AUDIO_OBJECT_TYPE_ER_HILN = 26  # Error Resilient HILN                         
    MPEG4_AUDIO_OBJECT_TYPE_ER_PARAMETRIC = 27  # Error Resilient Parametric                   
    MPEG4_AUDIO_OBJECT_TYPE_SSC = 28  # SSC                                          
    MPEG4_AUDIO_OBJECT_TYPE_PS = 29  # Parametric Stereo                            
    MPEG4_AUDIO_OBJECT_TYPE_MPEG_SURROUND = 30  # MPEG Surround                                
    MPEG4_AUDIO_OBJECT_TYPE_LAYER_1 = 32  # MPEG Layer 1                                 
    MPEG4_AUDIO_OBJECT_TYPE_LAYER_2 = 33  # MPEG Layer 2                                 
    MPEG4_AUDIO_OBJECT_TYPE_LAYER_3 = 34  # MPEG Layer 3                                 
    MPEG4_AUDIO_OBJECT_TYPE_DST = 35  # DST Direct Stream Transfer                   
    MPEG4_AUDIO_OBJECT_TYPE_ALS = 36  # ALS Lossless Coding                          
    MPEG4_AUDIO_OBJECT_TYPE_SLS = 37  # SLS Scalable Lossless Coding                 
    MPEG4_AUDIO_OBJECT_TYPE_SLS_NON_CORE = 38  # SLS Sclable Lossless Coding Non-Core         
    MPEG4_AUDIO_OBJECT_TYPE_ER_AAC_ELD = 39  # Error Resilient AAC ELD                      
    MPEG4_AUDIO_OBJECT_TYPE_SMR_SIMPLE = 40  # SMR Simple                                   
    MPEG4_AUDIO_OBJECT_TYPE_SMR_MAIN = 41  # SMR Main
    MPEG4_AUDIO_OBJECT_TYPE_USAC = 42  # USAC
    MPEG4_AUDIO_OBJECT_TYPE_SAOC = 43  # SAOC

    ERROR_INVALID_FORMAT = -1

    UNKNOWN = None

    @classmethod
    def _missing_(cls, value):
        return AudioObjectType.UNKNOWN
