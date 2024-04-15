import strawberry

from gqlauth.user import arg_mutations as mutations 


@strawberry.type
class Mutation:
    token_auth = mutations.ObtainJSONWebToken.field
    refresh_token = mutations.RefreshToken.field

    # verify_account = mutations.VerifyAccount.field
    # # include what-ever mutations you want.
    # verify_token = mutations.VerifyToken.field
    # update_account = mutations.UpdateAccount.field
    # archive_account = mutations.ArchiveAccount.field
    # delete_account = mutations.DeleteAccount.field
    # password_change = mutations.PasswordChange.field
    # swap_emails = mutations.SwapEmails.field
    # captcha = Captcha.field


#     register = mutations.Register.field
#     resend_activation_email = mutations.ResendActivationEmail.field
#     send_password_reset_email = mutations.SendPasswordResetEmail.field
#     password_reset = mutations.PasswordReset.field
#     password_set = mutations.PasswordSet.field
#     revoke_token = mutations.RevokeToken.field
#     verify_secondary_email = mutations.VerifySecondaryEmail.field
