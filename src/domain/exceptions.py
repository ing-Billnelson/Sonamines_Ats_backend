"""Exceptions du domaine métier."""


class DomainException(Exception):
    """Exception de base pour les erreurs du domaine métier."""

    pass


class CandidatureNonEligibleError(DomainException):
    """Erreur levée quand une candidature n'est pas éligible."""

    def __init__(self, message: str = "Cette candidature n'est pas éligible"):
        super().__init__(message)
        self.message = message


class OffreClotureeError(DomainException):
    """Erreur levée quand on tente d'interagir avec une offre clôturée."""

    def __init__(self, message: str = "Cette offre est clôturée"):
        super().__init__(message)
        self.message = message


class CanalNonVerifieError(DomainException):
    """Erreur levée quand le canal de notification n'est pas vérifié."""

    def __init__(self, canal: str, message: str = ""):
        if not message:
            message = f"Le canal {canal} n'est pas vérifié pour cet utilisateur"
        super().__init__(message)
        self.canal = canal
        self.message = message


class FichierTropVolumineuxError(DomainException):
    """Erreur levée quand un fichier dépasse la taille autorisée."""

    def __init__(
        self,
        taille_actuelle: int,
        taille_max: int,
        categorie: str,
        message: str = "",
    ):
        if not message:
            taille_mb_actuelle = taille_actuelle / (1024 * 1024)
            taille_mb_max = taille_max / (1024 * 1024)
            message = (
                f"Fichier trop volumineux pour la catégorie {categorie}: "
                f"{taille_mb_actuelle:.1f} MB (maximum: {taille_mb_max:.1f} MB)"
            )
        super().__init__(message)
        self.taille_actuelle = taille_actuelle
        self.taille_max = taille_max
        self.categorie = categorie
        self.message = message


class FormatFichierNonSupporteError(DomainException):
    """Erreur levée quand le format d'un fichier n'est pas supporté."""

    def __init__(
        self,
        format_actuel: str,
        formats_autorises: list[str],
        categorie: str,
        message: str = "",
    ):
        if not message:
            formats_str = ", ".join(formats_autorises)
            message = (
                f"Format {format_actuel} non supporté pour la catégorie {categorie}. "
                f"Formats autorisés: {formats_str}"
            )
        super().__init__(message)
        self.format_actuel = format_actuel
        self.formats_autorises = formats_autorises
        self.categorie = categorie
        self.message = message


class UtilisateurExistantError(DomainException):
    """Erreur levée quand on tente de créer un utilisateur déjà existant."""

    def __init__(self, email: str, message: str = ""):
        if not message:
            message = f"Un utilisateur avec l'email {email} existe déjà"
        super().__init__(message)
        self.email = email
        self.message = message


class UtilisateurIntrouvableError(DomainException):
    """Erreur levée quand un utilisateur n'est pas trouvé."""

    def __init__(self, identifiant: str, message: str = ""):
        if not message:
            message = f"Utilisateur introuvable: {identifiant}"
        super().__init__(message)
        self.identifiant = identifiant
        self.message = message


class OffreIntrouvableError(DomainException):
    """Erreur levée quand une offre n'est pas trouvée."""

    def __init__(self, identifiant: str, message: str = ""):
        if not message:
            message = f"Offre introuvable: {identifiant}"
        super().__init__(message)
        self.identifiant = identifiant
        self.message = message


class CandidatureIntrouvableError(DomainException):
    """Erreur levée quand une candidature n'est pas trouvée."""

    def __init__(self, identifiant: str, message: str = ""):
        if not message:
            message = f"Candidature introuvable: {identifiant}"
        super().__init__(message)
        self.identifiant = identifiant
        self.message = message


class CodeValidationInvalideError(DomainException):
    """Erreur levée quand le code de validation est incorrect ou expiré."""

    def __init__(self, message: str = "Code de validation incorrect ou expiré"):
        super().__init__(message)
        self.message = message


class StatutCandidatureInvalideError(DomainException):
    """Erreur levée lors d'une transition de statut invalide."""

    def __init__(
        self, statut_actuel: str, statut_demande: str, message: str = ""
    ):
        if not message:
            message = (
                f"Transition de statut invalide: "
                f"de {statut_actuel} vers {statut_demande}"
            )
        super().__init__(message)
        self.statut_actuel = statut_actuel
        self.statut_demande = statut_demande
        self.message = message


class AuthentificationEchoueeError(DomainException):
    """Erreur levée lors d'un échec d'authentification."""

    def __init__(self, message: str = "Échec de l'authentification"):
        super().__init__(message)
        self.message = message


class AutorisationRefuseeError(DomainException):
    """Erreur levée quand une opération n'est pas autorisée."""

    def __init__(self, message: str = "Opération non autorisée"):
        super().__init__(message)
        self.message = message