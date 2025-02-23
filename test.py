ssml = f"""
                                <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
                                    <voice name='123'>
                                        <prosody pitch='+25%'>
                                            123
                                        </prosody>
                                    </voice>
                                </speak>
                                """
# 生成 SSML 並轉義 XML
ssml = ssml.format(
voice_name,
escape(text)
)