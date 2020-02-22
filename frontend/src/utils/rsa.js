import JSEncrypt from 'jsencrypt'

export function encrypt(password) {
  const jsenObj = new JSEncrypt()
  jsenObj.setPublicKey('-----BEGIN PUBLIC KEY-----\n' +
    'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCjvd4MLih1sYRkQ3AmTc3XnzpE\n' +
    '/zNAiGexrxBWB8GpQ8+a04dcmX7ELIpGesxkmNERZXJcvbIbhy+ylQwpGGXbau6X\n' +
    'TIEMhz/Adi8XbOaMPrPOjJrzvr1A313CLx8+qO0cLi08fBly/1LCEwBfJiEDab+e\n' +
    'Gcd0G51ov35Bmr/SeQIDAQAB\n' +
    '-----END PUBLIC KEY-----')
  return jsenObj.encrypt(password)
}
