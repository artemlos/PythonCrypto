using System;
using Microsoft.VisualStudio.TestTools.UnitTesting;

using AES;
namespace UnitTestProject1
{
    [TestClass]
    public class UnitTest1
    {
        [TestMethod]
        public void TestMethod1()
        {
            // F295B9318B994434D93D98A4E449AFD8
            var a = Program.KeyExpansion(Convert.FromBase64String("8pW5MYuZRDTZPZik5Emv2A=="));
        }

        [TestMethod]
        public void Encrypt()
        {
            var a = Program.KeyExpansion(Convert.FromBase64String("9MAgoKH2BP00P6xqfmrg+Q=="));
            var message = Convert.FromBase64String("8pW5MYuZRDTZPZik5Emv2A==");
            Program.EncryptBlock(ref message, a);


        }
    }
}
