using System;
using System.Configuration;
using System.Security.Cryptography;
using System.Text;

namespace SyncLocation
{
	public static class Crypto
	{
		public static string decrypt(string cipherString, bool useHashing)
		{
				byte[] array = Convert.FromBase64String(cipherString);
				AppSettingsReader appSettingsReader = new AppSettingsReader();
				// string SecurityKey = (string)appSettingsReader.GetValue("SecurityKey", typeof(string));
				string SecurityKey = "_5TL#+GWWFv6pfT3!GXw7D86pkRRTv+$$tk^cL5hdU%";
				byte[] key;
				
				if (useHashing)
				{
						MD5CryptoServiceProvider md5CryptoServiceProvider = new MD5CryptoServiceProvider();
						key = md5CryptoServiceProvider.ComputeHash(Encoding.UTF8.GetBytes(SecurityKey));
						md5CryptoServiceProvider.Clear();
				}
				
				else
				{
						key = Encoding.UTF8.GetBytes(SecurityKey);
				}
				
				TripleDESCryptoServiceProvider tripleDESCryptoServiceProvider = new TripleDESCryptoServiceProvider();
				tripleDESCryptoServiceProvider.Key = key;
				tripleDESCryptoServiceProvider.Mode = CipherMode.ECB;
				tripleDESCryptoServiceProvider.Padding = PaddingMode.PKCS7;
				ICryptoTransform cryptoTransform = tripleDESCryptoServiceProvider.CreateDecryptor();
				byte[] bytes = cryptoTransform.TransformFinalBlock(array, 0, array.Length);
				tripleDESCryptoServiceProvider.Clear();
				return Encoding.UTF8.GetString(bytes);
		}
		
		static public void Main(String[] args) 
		{
			Console.Write("Username : "+decrypt("USERNAME", true));
			Console.Write("\n");
			Console.Write("Password : "+decrypt("PASSWORD", true));
		}	
	}
}
